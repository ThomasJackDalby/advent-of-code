const string INPUT_FILE_NAME = "input.txt";
const string TEST_FILE_NAME = "test.txt";
const string PROGRAM_TEMPLATE_FILE_PATH = "Program.template";
const string PROGRAM_FILE_NAME = "Program.cs";
const string PROJECT_TEMPLATE_FILE_PATH = "Project.template";
const string PROJECT_FILE_NAME = "Day{0:00}.csproj";
const string AOC_REPOSITORY_LOCATION = "AOC_REPOSITORY_LOCATION";

static void Warning(string message)
{
    Console.ForegroundColor = ConsoleColor.DarkYellow;
    Console.WriteLine(message);
    Console.ForegroundColor = ConsoleColor.Gray;
}

static int Error(string message, int errorCode = -1)
{
    Console.ForegroundColor = ConsoleColor.Red;
    Console.Error.WriteLine(message);
    Console.ForegroundColor = ConsoleColor.Gray;
    return errorCode;
}

if (args.Length < 2) throw new Exception("A year must be specified.");
if (args.Length < 3) throw new Exception("A day must be specified.");

int year = Int32.Parse(args[1]);
int day = Int32.Parse(args[2]);

string? rootFolderPath = Environment.GetEnvironmentVariable("AOC_REPOSITORY_LOCATION");
if (rootFolderPath is null) return Error($"The environment variable [{AOC_REPOSITORY_LOCATION}] must be set.");
if (!Directory.Exists(rootFolderPath)) return Error($"Repository folder [{rootFolderPath}] doesn't exist.");

string targetFolderPath = Path.Join(rootFolderPath, $"{year}", $"{day:00}");
if (!Directory.Exists(targetFolderPath))
{
    Directory.CreateDirectory(targetFolderPath);
    Console.WriteLine($"Created [{targetFolderPath}].");
}
else Warning($"[{targetFolderPath}] already exists.");

void CreateFile(string targetFilePath, string fileContents)
{
    if (!File.Exists(targetFilePath))
    {
        File.WriteAllText(targetFilePath, fileContents);
        Console.WriteLine($"Created [{targetFilePath}].");
    }
    else Warning($"[{targetFilePath}] already exists.");
}

string projectFilePath = Path.Join(targetFolderPath, String.Format(PROJECT_FILE_NAME, day));
string projectFileContents = String.Format(File.ReadAllText(PROJECT_TEMPLATE_FILE_PATH), day);
CreateFile(projectFilePath, projectFileContents);

string programFilePath = Path.Join(targetFolderPath, PROGRAM_FILE_NAME);
string template = File.ReadAllText(PROGRAM_TEMPLATE_FILE_PATH);
string programFileContents = String.Format(template, year, day, DateTime.Now);
CreateFile(programFilePath, programFileContents);

string inputFilePath = Path.Join(targetFolderPath, INPUT_FILE_NAME);
CreateFile(inputFilePath, "");

string testFilePath = Path.Join(targetFolderPath, TEST_FILE_NAME);
CreateFile(testFilePath, "");

return 0;