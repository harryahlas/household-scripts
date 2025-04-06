import os
import sys
import subprocess
import webview
import json
import threading

# HTML content for the user interface remains the same as before
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WMA to MP3 Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        input[type="text"], select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 16px;
        }
        
        .file-input-container {
            display: flex;
            gap: 10px;
        }
        
        .file-input-container input[type="text"] {
            flex-grow: 1;
        }
        
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        
        button:hover {
            background-color: #45a049;
        }
        
        .browse-button {
            background-color: #2196F3;
        }
        
        .browse-button:hover {
            background-color: #0b7dda;
        }
        
        .convert-button {
            display: block;
            width: 100%;
            margin-top: 30px;
            font-weight: bold;
        }
        
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 4px;
            display: none;
        }
        
        .success {
            background-color: #dff0d8;
            border: 1px solid #d6e9c6;
            color: #3c763d;
        }
        
        .error {
            background-color: #f2dede;
            border: 1px solid #ebccd1;
            color: #a94442;
        }
        
        .progress-container {
            margin-top: 20px;
            display: none;
        }
        
        progress {
            width: 100%;
            height: 20px;
        }
        
        .settings-toggle {
            color: #2196F3;
            cursor: pointer;
            display: block;
            margin-top: 20px;
            text-align: center;
        }
        
        .advanced-settings {
            display: none;
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>WMA to MP3 Converter</h1>
        
        <div class="form-group">
            <label for="input-file">WMA File to Convert:</label>
            <div class="file-input-container">
                <input type="text" id="input-file" placeholder="Select a WMA file...">
                <button class="browse-button" id="browse-input">Browse</button>
            </div>
        </div>
        
        <div class="form-group">
            <label for="output-dir">Output Directory:</label>
            <div class="file-input-container">
                <input type="text" id="output-dir" value="D:\\Music\\mp3s\\" placeholder="Select output directory...">
                <button class="browse-button" id="browse-output">Browse</button>
            </div>
        </div>
        
        <div class="form-group">
            <label for="output-filename">Output Filename:</label>
            <input type="text" id="output-filename" placeholder="[Same as input filename]">
        </div>
        
        <div class="settings-toggle" id="settings-toggle">Advanced Settings ▼</div>
        
        <div class="advanced-settings" id="advanced-settings">
            <div class="form-group">
                <label for="bitrate">Bitrate:</label>
                <select id="bitrate">
                    <option value="320k">320 kbps (High Quality)</option>
                    <option value="256k">256 kbps</option>
                    <option value="192k">192 kbps</option>
                    <option value="128k">128 kbps (Standard Quality)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="ffmpeg-path">FFmpeg Path (if not in system PATH):</label>
                <div class="file-input-container">
                    <input type="text" id="ffmpeg-path" placeholder="Path to ffmpeg executable...">
                    <button class="browse-button" id="browse-ffmpeg">Browse</button>
                </div>
            </div>
        </div>
        
        <button class="convert-button" id="convert-button">Convert WMA to MP3</button>
        
        <div class="progress-container" id="progress-container">
            <p>Converting... Please wait.</p>
            <progress id="progress-bar" max="100" value="0"></progress>
        </div>
        
        <div class="status" id="status"></div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Elements
            const inputFileEl = document.getElementById('input-file');
            const outputDirEl = document.getElementById('output-dir');
            const outputFilenameEl = document.getElementById('output-filename');
            const browseInputBtn = document.getElementById('browse-input');
            const browseOutputBtn = document.getElementById('browse-output');
            const browseFFmpegBtn = document.getElementById('browse-ffmpeg');
            const convertBtn = document.getElementById('convert-button');
            const progressContainer = document.getElementById('progress-container');
            const progressBar = document.getElementById('progress-bar');
            const statusEl = document.getElementById('status');
            const settingsToggle = document.getElementById('settings-toggle');
            const advancedSettings = document.getElementById('advanced-settings');
            const bitrateEl = document.getElementById('bitrate');
            const ffmpegPathEl = document.getElementById('ffmpeg-path');
            
            // Default output directory
            const defaultOutputDir = "D:\\\\Music\\\\mp3s\\\\";
            
            // Toggle advanced settings
            settingsToggle.addEventListener('click', function() {
                if (advancedSettings.style.display === 'block') {
                    advancedSettings.style.display = 'none';
                    settingsToggle.textContent = 'Advanced Settings ▼';
                } else {
                    advancedSettings.style.display = 'block';
                    settingsToggle.textContent = 'Advanced Settings ▲';
                }
            });
            
            // Handle input file selection
            browseInputBtn.addEventListener('click', function() {
                pywebview.api.browse_wma_file().then(function(filePath) {
                    if (filePath) {
                        inputFileEl.value = filePath;
                        
                        // Extract filename for output
                        const fileName = filePath.split('\\\\').pop().split('/').pop();
                        const fileNameWithoutExt = fileName.substring(0, fileName.lastIndexOf('.'));
                        outputFilenameEl.value = fileNameWithoutExt + ".mp3";
                    }
                });
            });
            
            // Handle output directory selection
            browseOutputBtn.addEventListener('click', function() {
                pywebview.api.browse_directory().then(function(dirPath) {
                    if (dirPath) {
                        outputDirEl.value = dirPath.endsWith('\\\\') ? dirPath : dirPath + '\\\\';
                    }
                });
            });
            
            // Handle ffmpeg path selection
            browseFFmpegBtn.addEventListener('click', function() {
                pywebview.api.browse_ffmpeg_file().then(function(filePath) {
                    if (filePath) {
                        ffmpegPathEl.value = filePath;
                    }
                });
            });
            
            // Convert button click
            convertBtn.addEventListener('click', function() {
                // Validate inputs
                if (!inputFileEl.value) {
                    showStatus("Please select a WMA file to convert.", "error");
                    return;
                }
                
                if (!outputDirEl.value) {
                    outputDirEl.value = defaultOutputDir;
                }
                
                // Prepare conversion parameters
                const params = {
                    inputFile: inputFileEl.value,
                    outputDir: outputDirEl.value,
                    outputFilename: outputFilenameEl.value,
                    bitrate: bitrateEl.value,
                    ffmpegPath: ffmpegPathEl.value
                };
                
                // Show progress
                progressContainer.style.display = 'block';
                statusEl.style.display = 'none';
                convertBtn.disabled = true;
                
                // Start conversion
                pywebview.api.convert_file(params).then(function(result) {
                    progressContainer.style.display = 'none';
                    convertBtn.disabled = false;
                    
                    if (result.success) {
                        showStatus(`Conversion completed successfully!<br><br>Input: ${params.inputFile}<br>Output: ${result.outputFile}<br>Bitrate: ${params.bitrate}`, "success");
                    } else {
                        showStatus(`Error: ${result.error}`, "error");
                    }
                });
                
                // Set up progress updates
                const progressUpdater = setInterval(function() {
                    pywebview.api.get_progress().then(function(progress) {
                        progressBar.value = progress;
                        
                        if (progress >= 100) {
                            clearInterval(progressUpdater);
                        }
                    });
                }, 500);
            });
            
            // Helper function to show status messages
            function showStatus(message, type) {
                statusEl.innerHTML = message;
                statusEl.className = "status " + type;
                statusEl.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""

class Api:
    def __init__(self):
        self.progress = 0
        self.conversion_thread = None
    
    def browse_wma_file(self):
        """Open a file browser dialog to select a WMA file"""
        # Fix: Changed the file_types format to match what webview expects
        file_types = ('WMA files (*.wma)',)
        result = window.create_file_dialog(webview.OPEN_DIALOG, file_types=file_types)
        
        if result and len(result) > 0:
            return result[0]
        return None
    
    def browse_ffmpeg_file(self):
        """Open a file browser dialog to select the ffmpeg executable"""
        # Fix: Changed the file_types format to match what webview expects
        file_types = ('Executable files (*.exe)',)
        result = window.create_file_dialog(webview.OPEN_DIALOG, file_types=file_types)
        
        if result and len(result) > 0:
            return result[0]
        return None
    
    def browse_directory(self):
        """Open a directory browser dialog"""
        result = window.create_file_dialog(webview.FOLDER_DIALOG)
        if result and len(result) > 0:
            return result[0]
        return None
    
    def get_progress(self):
        """Get current conversion progress"""
        return self.progress
    
    def convert_file(self, params):
        """Convert WMA file to MP3 using ffmpeg"""
        self.progress = 0
        input_file = params['inputFile']
        output_dir = params['outputDir']
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                return {'success': False, 'error': f"Failed to create output directory: {str(e)}"}
        
        # Handle output filename
        if params['outputFilename']:
            output_filename = params['outputFilename']
            if not output_filename.endswith('.mp3'):
                output_filename += '.mp3'
        else:
            # Extract filename without extension
            input_filename = os.path.basename(input_file)
            name_without_ext = os.path.splitext(input_filename)[0]
            output_filename = f"{name_without_ext}.mp3"
        
        output_file = os.path.join(output_dir, output_filename)
        
        # Set ffmpeg path
        ffmpeg_cmd = params['ffmpegPath'] if params['ffmpegPath'] else 'ffmpeg'
        
        # Build the ffmpeg command
        cmd = [
            ffmpeg_cmd,
            '-i', input_file,
            '-codec:a', 'libmp3lame',
            '-b:a', params['bitrate'],
            '-y',  # Overwrite output file if it exists
            output_file
        ]
        
        # Start conversion in a separate thread
        self.conversion_thread = threading.Thread(
            target=self._run_conversion, 
            args=(cmd, output_file)
        )
        self.conversion_thread.start()
        
        return {'success': True, 'outputFile': output_file}
    
    def _run_conversion(self, cmd, output_file):
        """Run the actual conversion process"""
        try:
            # Start the conversion process
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Simulate progress (ffmpeg doesn't provide easy progress info)
            # In a real app, you might parse ffmpeg output to get actual progress
            for i in range(0, 101, 5):
                self.progress = i
                time.sleep(0.2)  # Simulate processing time
            
            # Wait for process to complete
            stdout, stderr = process.communicate()
            
            # Check if output file was created successfully
            if process.returncode != 0 or not os.path.exists(output_file):
                self.progress = 0
                print(f"Error during conversion: {stderr}")
            else:
                self.progress = 100
                print(f"Conversion completed successfully: {output_file}")
                
        except Exception as e:
            self.progress = 0
            print(f"Exception during conversion: {str(e)}")

if __name__ == '__main__':
    # Fix for pyinstaller packaging
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
    
    # Import time here to avoid potential circular import
    import time
    
    api = Api()
    window = webview.create_window('WMA to MP3 Converter', html=HTML, js_api=api, min_size=(700, 600))
    webview.start()