library(pdftools)

pdf_files <- c("C:\\Users\\Anyone\\Desktop\\Scan1-4.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan5.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan6.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan7-9.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan10b.pdf")

pdf_output <- "C:\\Users\\Anyone\\Desktop\\ScanForVictoria.pdf"

pdf_combine(pdf_files, pdf_output)


library(mailR)
send.mail(from = "___@hotmail.com",
          to = c("___@aol.com"),
          subject = "scans",
          body = "scans from ____",
          smtp = list(host.name = "smtp.live.com",  
                      port = "587", 
                      user.name = "_____@hotmail.com", 
                      passwd = rstudioapi::askForPassword("password:"), 
                      tls = TRUE
          ),
          authenticate = TRUE,
          send = TRUE,
          attach.files = pdf_output, 
          #file.names = c("Download log.log", "Upload log.log", "DropBox File.rtf"), # optional parameter
          #file.descriptions = c("Description for download log", "Description for upload log", "DropBox File"), # optional parameter
          debug = TRUE)
