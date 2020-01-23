library(pdftools)

pdf_files <- c("C:\\Users\\Anyone\\Desktop\\Scan1-4.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan5.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan6.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan7-9.pdf",
              "C:\\Users\\Anyone\\Desktop\\Scan10b.pdf")

pdf_output <- "C:\\Users\\Anyone\\Desktop\\ScanForVictoria.pdf"

pdf_combine(pdf_files, pdf_output)
