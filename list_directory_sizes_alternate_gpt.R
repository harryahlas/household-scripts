# Load necessary library
if (!requireNamespace("fs", quietly = TRUE)) install.packages("fs")
library(fs)

# Function to safely list directories, catching errors and returning an empty list if an error occurs
safe_dir_ls <- function(path) {
  tryCatch({
    fs::dir_ls(path, type = "directory")
  }, error = function(e) {
    message("Skipping inaccessible directory: ", path)
    return(character(0)) # Return an empty character vector if error
  })
}

# Function to recursively list directories up to a certain depth, with error handling
list_dirs <- function(path, max_depth = 3, current_depth = 1) {
  if (current_depth > max_depth) {
    return(character(0))
  }
  
  dirs <- safe_dir_ls(path)
  deeper_dirs <- lapply(dirs, function(d) list_dirs(d, max_depth, current_depth + 1))
  return(c(dirs, unlist(deeper_dirs)))
}

# Function to calculate the size of a directory, catching errors for each file
calc_dir_size <- function(dir_path) {
  files <- tryCatch({
    fs::dir_ls(dir_path, recurse = TRUE, type = "file")
  }, error = function(e) {
    message("Skipping inaccessible files in: ", dir_path)
    return(character(0)) # Return an empty character vector if error
  })
  
  total_size <- 0
  for (file_path in files) {
    file_size <- tryCatch({
      fs::file_info(file_path)$size
    }, error = function(e) {
      message("Skipping inaccessible file: ", file_path)
      return(0) # Return 0 size if error
    })
    total_size <- total_size + file_size
  }
  
  return(total_size)
}

# Use the updated list_dirs function to safely list directories within 3 levels of the C drive
dirs <- list_dirs("C:/", max_depth = 3)

# Calculate sizes and filter directories greater than 1GB (1GB = 1e9 bytes)
large_dirs <- sapply(dirs, calc_dir_size, simplify = "array", USE.NAMES = TRUE)
large_dirs <- large_dirs[large_dirs > 1e9]

# Create a data frame of directories larger than 1GB
output_df <- data.frame(Directory = names(large_dirs), Size_GB = large_dirs / 1e9)

# Write the results to a CSV file
write.csv(output_df, "large_directories.csv", row.names = FALSE)

message("CSV file has been created with directories greater than 1GB.")
