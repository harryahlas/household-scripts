# Load necessary library
if (!requireNamespace("fs", quietly = TRUE)) install.packages("fs")
library(fs)

# Function to recursively list directories up to a certain depth
list_dirs <- function(path, max_depth = 3, current_depth = 1) {
  if (current_depth > max_depth) {
    return(NULL)
  }
  
  dirs <- fs::dir_ls(path, type = "directory")
  deeper_dirs <- lapply(dirs, function(d) list_dirs(d, max_depth, current_depth + 1))
  return(c(dirs, unlist(deeper_dirs)))
}

# Function to calculate the size of a directory
calc_dir_size <- function(dir_path) {
  files <- fs::dir_ls(dir_path, recurse = TRUE, type = "file")
  total_size <- sum(fs::file_info(files)$size)
  return(total_size)
}

# List all directories within 3 levels of the C drive
dirs <- list_dirs("C:/", max_depth = 3)

# Calculate sizes and filter directories greater than 1GB (1GB = 1e9 bytes)
large_dirs <- sapply(dirs, calc_dir_size)
large_dirs <- large_dirs[large_dirs > 1e9]

# Create a data frame
output_df <- data.frame(Directory = names(large_dirs), Size_GB = large_dirs / 1e9)

# Write to CSV
write.csv(output_df, "large_directories.csv", row.names = FALSE)

print("CSV file has been created with directories greater than 1GB.")
