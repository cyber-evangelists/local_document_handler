using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DocService
{
    public static class BaseURL
    {
        private static string baseUrl = "https://beed-223-123-13-51.ngrok-free.app";

        public static string UploadFile = baseUrl + "/upload_file";

        public static string Get_File = baseUrl + "/get_file";
    }
}
