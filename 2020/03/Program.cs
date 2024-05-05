



Map LoadInputFile(string filePath) 
{
    if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
    using Stream stream = File.Open(filePath, FileMode.Open, FileAccess.Read);
    using StreamReader reader = new(stream);
    List<string> data = new();
    while(!reader.EndOfStream)
    {
        string? line = reader.ReadLine();
        if (line is null) continue;
        data.Add(line.Trim());a
    }
    if (data.Count == 0) throw new Exception("Unable to load data from file.");
    return new Map(data.ToArray());
}

const char TILE_TREE = '#';

int SolveSlope(Map data, int dx, int dy) {
    int numberOfTrees = 0;
    int x = 0;
    int y = 0;
    while (y < data.Height) {
        if (data.Get(x, y) == TILE_TREE) numberOfTrees++;
        x += dx;
        y += dy;
    }
    return numberOfTrees;
}

int SolvePart1(Map data) {
    return SolveSlope(data, 3, 1);
}
int SolvePart2(Map data) {
    (int X, int Y)[] slopes = new[] {
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    };
    return slopes
        .Select(slope => SolveSlope(data, slope.X, slope.Y))
        .Aggregate((total, result) => total * result);
}

Map data = LoadInputFile("input.txt");
Console.WriteLine($"Part 1: {SolvePart1(data)}");
Console.WriteLine($"Part 2: {SolvePart2(data)}");

public readonly record struct Map(string[] Data)
{
    public int Height { get; } = Data.Length;
    public int Width { get; } = Data[0].Length;

    public char Get(int x, int y) {
        return Data[y][x % Width];
    }
}