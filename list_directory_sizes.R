

path_of_directory <-  sub_directories[8]


getDirectorySize <- function(path_of_directory){
  files<-list.files(path_of_directory,full.names = T,all.files = T,include.dirs = T,recursive = T)
  if(length(files) == 0) {
    print(paste("ERROR!! no files found in ", path_of_directory))}
  else {
    vect_size <- sapply(files, file.size)
    size_files <- sum(vect_size, na.rm = T)
    print(paste(round(size_files/1000000000,1), "Gb found in directory:", path_of_directory))
  }
}


base_directory <- "C:\\ProgramData\\"

sub_directories <- list.dirs(base_directory, recursive = F)

lapply(sub_directories[9:length(sub_directories)], getDirectorySize)






getDirectorySize(sub_directories[8])


getDirectorySize("C:\\ProgramData\\Steinberg\\")
