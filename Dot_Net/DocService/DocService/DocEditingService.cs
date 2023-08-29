using Microsoft.Win32.TaskScheduler;
using System;
using System.ComponentModel;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Management;
using System.ServiceProcess;
using System.Text.RegularExpressions;
using System.Threading;

namespace DocService
{
    [RunInstaller(true)]
    public partial class DocEditingService : ServiceBase
    {
        private string DownloadFolderPath = string.Empty;
        private string DownloadedFileName = string.Empty;
        private string DomnainAndUserName = string.Empty;

        private readonly string _databaseConnectionString = "Data Source=localhost;Initial Catalog=DMS;Integrated Security=True;TrustServerCertificate=True";

        private FileSystemWatcher _fileWatcher;

        public DocEditingService()
        {
            InitializeComponent();
        }

        #region On Service start
        protected override void OnStart(string[] args)
        {
            try
            {
                GetDownloadAndUserName();

                _fileWatcher = new FileSystemWatcher(DownloadFolderPath);
                _fileWatcher.Renamed += OnRenamed;
                _fileWatcher.EnableRaisingEvents = true;

            }
            catch (Exception ex)
            {
                LogMessage($"Error downloading document with ID 0: {ex.ToString()}", EventLogEntryType.Error);

            }
        }
        #endregion

        #region Main File Related Things
        private void ProcessRequest()
        {
            try
            {
                if (!string.IsNullOrEmpty(DownloadedFileName))
                {
                    int docId = GetDocumentIdByName(DownloadedFileName);
                    string fullPath = string.Empty;

                    try
                    {

                        fullPath = Path.Combine(DownloadFolderPath, DownloadedFileName);

                        if (File.Exists(fullPath))
                        {
                            try
                            {
                                CreateHighPriorityTask(fullPath);
                                WaitForDocumentClose(fullPath);
                                SaveDocument(fullPath, docId);

                            }

                            catch (Exception ex)
                            {
                                LogMessage($"An error occurred: {ex.Message}", EventLogEntryType.Error);
                            }
                        }
                        else
                        {
                            LogMessage($"File not found: {fullPath}", EventLogEntryType.Information);
                        }
                    }
                    catch (Exception ex)
                    {
                        LogMessage($"Error in Opening File {ex.Message}", EventLogEntryType.Information);
                    }

                }
            }
            catch (Exception ex)
            {
                LogMessage($"Error in Opening File {ex.Message}", EventLogEntryType.Information);
            }
        }

        private void CreateHighPriorityTask(string fullPath)
        {
            try
            {
                using (TaskService taskService = new TaskService())
                {
                    TaskDefinition taskDefinition = taskService.NewTask();
                    taskDefinition.RegistrationInfo.Description = "Document Editing Process";
                    taskDefinition.RegistrationInfo.Author = "SYSTEM";

                    taskDefinition.Principal.DisplayName = "Document Edit Service";
                    taskDefinition.Principal.RunLevel = TaskRunLevel.Highest;
                    taskDefinition.Principal.GroupId = "User";
                    taskDefinition.Principal.UserId = DomnainAndUserName;
                    taskDefinition.Principal.LogonType = TaskLogonType.InteractiveToken;

                    taskDefinition.Settings.AllowDemandStart = true;
                    taskDefinition.Settings.AllowHardTerminate = true;
                    taskDefinition.Settings.DisallowStartIfOnBatteries = false;
                    taskDefinition.Settings.DisallowStartOnRemoteAppSession = true;
                    taskDefinition.Settings.Hidden = false;
                    taskDefinition.Settings.RestartCount = 0;
                    taskDefinition.Settings.RunOnlyIfIdle = false;
                    taskDefinition.Settings.RunOnlyIfNetworkAvailable = false;
                    taskDefinition.Settings.StartWhenAvailable = true;
                    taskDefinition.Settings.StopIfGoingOnBatteries = false;
                    taskDefinition.Settings.Volatile = false;
                    taskDefinition.Settings.WakeToRun = false;
                    // Determine the file extension of the document
                    string fileExtension = System.IO.Path.GetExtension(fullPath).ToLower();

                    // Check if Word is the default application for the file extension
                    if (IsWordDefaultForExtension(fileExtension))
                    {
                        taskDefinition.Actions.Add(new ExecAction(fullPath, "winword.exe"));
                    }
                    else
                    {
                        taskDefinition.Actions.Add(new ExecAction(fullPath, "notepad.exe"));
                    }


                    const string taskName = "File Editing";
                    taskService.RootFolder.RegisterTaskDefinition(taskName, taskDefinition);

                    taskService.FindTask(taskName).Run();

                }

            }
            catch (Exception ex)
            {
                LogMessage($"Error Which Creating Editing Task:{ex.Message}", EventLogEntryType.Error);
            }
        }

        private bool IsWordDefaultForExtension(string extension)
        {
            using (Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.ClassesRoot.OpenSubKey(extension))
            {
                if (key != null)
                {
                    object defaultValue = key.GetValue(null);
                    return defaultValue != null && defaultValue.ToString().ToLower().Contains("word");
                }
            }

            LogMessage("its not working.", EventLogEntryType.Error);

            return false;

        }

        static string RemoveRepeatNumbers(string fileName)
        {
            // Use a regular expression to find and remove "(n)" pattern from the filename
            // where n is a number enclosed in parentheses.
            string cleanedFileName = Regex.Replace(fileName, @"\s+\(\d+\)", string.Empty);

            return cleanedFileName;
        }

        #endregion

        #region File Watcher things
        private void OnRenamed(object source, RenamedEventArgs e)
        {
            try
            {
                FileInfo file = new FileInfo(e.FullPath);
                DownloadedFileName = file.Name;
                if (!DownloadedFileName.Contains("crdownload"))
                {
                    ProcessRequest();
                }
            }
            catch (Exception ex)
            {
                LogMessage($"Error {ex.Message}", EventLogEntryType.Error);
            }
        }

        private void WaitForDocumentClose(string documentPath)
        {
            try
            {
                _fileWatcher = new FileSystemWatcher(Path.GetDirectoryName(documentPath));
                _fileWatcher.Filter = Path.GetFileName(documentPath);
                _fileWatcher.EnableRaisingEvents = true;
                _fileWatcher.Changed += OnFileChanged;

                // Wait for the file to be closed
                while (_fileWatcher.EnableRaisingEvents)
                {
                    Thread.Sleep(1000);
                }
            }
            catch(Exception ex)
            {
                LogMessage($"Error: {ex.ToString()}", EventLogEntryType.Error);

            }
        }

        private void OnFileChanged(object sender, FileSystemEventArgs e)
        {
            try
            {
                // If the file was closed, stop the file watcher
                if (e.ChangeType == WatcherChangeTypes.Changed)
                {
                    _fileWatcher.EnableRaisingEvents = false;
                    LogMessage($"File Edited Successfully.", EventLogEntryType.Information);

                }
            }
            catch(Exception ex)
            {
                LogMessage($"Something Went Wrong {ex.Message}.", EventLogEntryType.Error);

            }
        }

        #endregion

        #region SQL Queries
        private void SaveDocument(string documentPath, int docId)
        {
            if (File.Exists(documentPath))
            {
                byte[] documentData = File.ReadAllBytes(documentPath);

                using (var connection = new SqlConnection(_databaseConnectionString))
                {
                    connection.Open();

                    using (var cmd = new SqlCommand("UPDATE Documents SET Data = @DocumentData WHERE Id = @docId", connection))
                    {
                        cmd.Parameters.AddWithValue("@DocumentData", documentData);
                        cmd.Parameters.AddWithValue("@docId", docId);
                        cmd.ExecuteNonQuery();
                        connection.Close();
                    }
                }
            }
        }

        private int GetDocumentIdByName(string name)
        {
            try
            {
                int Id = 0;
                using (var connection = new SqlConnection(_databaseConnectionString))
                {
                    connection.Open();

                    name = RemoveRepeatNumbers(name);

                    using (var cmd = new SqlCommand("SELECT Id FROM Documents WHERE Name Like '%' + @DocumentName + '%'", connection))
                    {
                        cmd.Parameters.AddWithValue("@DocumentName", name);
                        var value = cmd.ExecuteScalar()?.ToString();
                        Id = Convert.ToInt32(value);

                        if (Id > 0)
                        {
                            connection.Close();
                            return Id;

                        }
                    }
                }

                LogMessage($"Document with this ID {Id} not found.", EventLogEntryType.Error);
                return 0;
            }
            catch (Exception ex)
            {
                LogMessage($"Error downloading document with Name {name}: {ex.ToString()}", EventLogEntryType.Error);
                return 0;

            }
        }

        #endregion

        #region UserName and Download Folder Property
        private void GetDownloadAndUserName()
        {
            try
            {
                ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT UserName FROM Win32_ComputerSystem");
                ManagementObjectCollection collection = searcher.Get();
                if (collection != null)
                {
                    DomnainAndUserName = (string)collection.Cast<ManagementBaseObject>().First()["UserName"];
                    var resultSet = DomnainAndUserName.Split('\\');
                    string username = resultSet[1];
                    DownloadFolderPath = string.Format(@"C:\Users\{0}\Downloads", username);

                }
            }
            catch(Exception ex)
            {
                LogMessage(ex.Message, EventLogEntryType.Error);

            }
        }
        #endregion

        #region Logging
        private void LogMessage(string message, EventLogEntryType entryType)
        {
            EventLog.WriteEntry("DocumentEditingService", message, entryType);
        }
        #endregion
    }
}

