using AdventOfCode2023.Day5;
using AdventOfCode2023.Extensions;
using System.Text;

var executablePath = System.AppDomain.CurrentDomain.BaseDirectory;
var dataPath = Path.GetFullPath(Path.Combine(executablePath, @"..\..\..\..\data"));
var Days = Enumerable.Range(1, 25);
var SkipDays = new int[] { 1, 2, 3, 4, 6, 7, 8 };
var StopBefore = 9;

var PrintDaySeparator = () => Console.WriteLine("=".Multiply(30));
var PrintContentSeparator = () => Console.WriteLine("=".Multiply(30));
var PrintDayHeader = (int day) => Console.WriteLine($"Day [{day}] - ".Multiply(4).RemoveSuffix(" - "));

bool RunExamples = true;
bool SkipExercise = false;

var GetFile = (string name) => new StreamReader(File.OpenRead(Path.Combine(dataPath, name)), Encoding.UTF8);

var GetExampleFile = (int day) => GetFile($"{day}_example.txt");
var GetExerciseFile = (int day) => GetFile($"{day}_input.txt");

foreach (var day in Days)
{
    if ( SkipDays.Contains(day))
    {
        continue;
    }
    if (day >= StopBefore)
    {
        continue;
    }
    PrintDaySeparator();
    PrintDayHeader(day);
    PrintContentSeparator();
       
    if (RunExamples)
    {
        Console.WriteLine("EXAMPLE");
        StreamReader example = GetExampleFile(day);

        
        Day5.Solution(example);
        
        PrintContentSeparator();
    }
    if(SkipExercise)
    {
        continue;
    }
    Console.WriteLine("EXERCISE");

    StreamReader exercise = GetExerciseFile(day);
    Day5.Solution(exercise);
}








Console.WriteLine(dataPath);