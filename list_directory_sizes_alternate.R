library(tidyverse)

list.dirs("C:\\Program Files (x86)", recursive = F)
file.info(list.files(path = '/my/directory/', recursive = T, full.names = T))$size

directories <- list.dirs("C:\\Program Files (x86)", recursive = F)

print(file.info(directories[5], ))





file.info("D:\\Music\\The Politics")$size

#https://stackoverflow.com/questions/39753172/compute-the-size-of-directory-in-r

dir_size <- function(path, recursive = TRUE) {
  stopifnot(is.character(path))
  files <- list.files(path, full.names = T, recursive = recursive)
  vect_size <- sapply(files, function(x) file.size(x))
  if(length(vect_size) == 0) {
    size_files <-  0} 
  else {
    size_files <- sum(vect_size)
  }
  size_files_formatted <- paste(round(size_files/1073741824, 2), "Gb")
  dir_sizes <<- dir_sizes %>% 
    add_row(directory = path, size = size_files, size_formatted = size_files_formatted)
}


dir_sizes <- data.frame(directory = as.character(), size = as.numeric(), size_formatted = as.character())


for (directory in list.dirs("C:\\Program Files", recursive = F)) {
  print(directory)
  print(dir_size(directory))
}



dir_size("C:\\Program Files (x86)\\apulSoft")/1000000000
dir_size("C:\\Program Files/IK Multimedia")


path <- "C:\\Program Files/IK Multimedia"
is.character("C:\\Program Files/IK Multimedia")
list.files("C:\\Program Files/IK Multimedia", full.names = T, recursive = T)
