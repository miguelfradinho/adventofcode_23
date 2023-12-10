using System.Numerics;

namespace AdventOfCode2023.Day5;

public class Day5
{
    /*
    public static BigInteger GetTransformation()
    {
        // small optim, if we find any, might as well use it
        var completeContain = currentIntervals.Where(x => seedStart >= x.Item1 && seedEnd <= x.Item2).SingleOrDefault();
        if (completeContain != default)
        {
            currNumber = completeContain.Item3 + (completeContain
            }
        // This is brute forcing, but by ignoring the non-overlapping intervals, we're removing a yuuuuge chunk of the iterations we have to do
        // same as (seedStart <= x.Item2 && seedEnd >= x.Item1) 

        var overlaps = currentIntervals.Where(x => !(seedEnd < x.Item1 || seedStart > x.Item2)).ToList();

        Console.WriteLine(completeContain.Count());
    }
    */

    /*
    public static BigInteger GetNumber()
    {
        // small optim, if we find any, might as well use it
        var completeContain = currentIntervals.Where(x => seedStart >= x.Item1 && seedEnd <= x.Item2).SingleOrDefault();
        if (completeContain != default)
        {
            currNumber = completeContain.Item3 + (completeContain
            }
        // This is brute forcing, but by ignoring the non-overlapping intervals, we're removing a yuuuuge chunk of the iterations we have to do
        // same as (seedStart <= x.Item2 && seedEnd >= x.Item1) 

        var overlaps = currentIntervals.Where(x => !(seedEnd < x.Item1 || seedStart > x.Item2)).ToList();

        Console.WriteLine(completeContain.Count());
    }
    */

    public static BigInteger SolveNaive(
        BigInteger initialValue, 
        string initialCategory, 
        string finalCategory, 
        IDictionary<string, string> categories,
        IDictionary<string, List<(BigInteger, BigInteger, BigInteger, BigInteger)>> almanac
        ) {
        var returnVal = initialValue;
        var currCategory = initialCategory;
        var currElem = initialValue;

        while(currCategory != finalCategory)
        {
            var nextCategory = categories[currCategory];

            foreach (var (start, end, dest_start, l) in almanac[currCategory])
            {
                if(start <= currElem && currElem <= end)
                {
                    currElem = dest_start + (currElem - start);
                    break;
                }
            }
            currCategory = nextCategory;
            returnVal = currElem;
        }
        return returnVal;
    }
    public static void Solution(StreamReader content)
    {
        var seeds = new List<BigInteger>();
        var categories = new Dictionary<string, string>();
        var almanac = new Dictionary<string, List<(BigInteger, BigInteger, BigInteger, BigInteger)>>();

        using (var f = content)
        {
            var seeds_line = f.ReadLine()!.Trim();
            seeds = seeds_line.Split(" ")[1..].Select(BigInteger.Parse).ToList();
            f.ReadLine();

            var mapLines = new List<string>();
            foreach(var l in f.ReadToEnd().Split("\n"))
            {
                var line = l.Trim();

                if (line.Length > 0)
                {
                    mapLines.Add(line);
                }
                else
                {
                    var header = mapLines[0].Split(" ")[0].Split("-to-");
                    var (source, destination) = (header[0], header[1]);
                    categories[source] = destination;

                    var rangeList = new List<(BigInteger, BigInteger, BigInteger, BigInteger)>();
                    foreach (var range in mapLines[1..])
                    {
                        var rangeParts = range.Split(" ").Select(BigInteger.Parse).ToList();
                        var (dest_start, source_start, length) = (rangeParts[0], rangeParts[1], rangeParts[2]);
                        var entry = (source_start, source_start + length - 1, dest_start, length);
                        rangeList.Add(entry);
                    }
                    rangeList.Sort((a,b) => a.Item1.CompareTo(b.Item1));
                    almanac.Add(source, rangeList);
                    mapLines.Clear();
                }
            }
        }

        const string startCategory = "seed";
        const string finalCategory = "location";

        var resultsPart1 = new List<BigInteger>();
        // Part 1
        foreach (var seed in seeds)
        {
            var result = SolveNaive(seed, startCategory, finalCategory, categories, almanac);
            resultsPart1.Add(result);
            Console.WriteLine($"{seed}, {result}");
        }
        Console.WriteLine($"Part 1 {resultsPart1.Min()}");


        // Part 2 Smart  but badly implemented?

        var rangesToCheck = new List<BigInteger>();

        // First pass, build the intervals we actually need to chec
        // maybe this works?
        var resultsPart2 = new List<BigInteger>();
        for (int i = 0; i < seeds.Count; i += 2)
        {
            var seedStart = seeds[i];
            var seedLength = seeds[i + 1];
            var seedEnd = seedStart + seedLength - 1;




        
            return;

            for (BigInteger seed = seedStart; seed <= seedEnd; seed++)
            {
                var result = SolveNaive(seed, startCategory, finalCategory, categories, almanac);
                // resultsPart1.Add(result);
                //Console.WriteLine($"{seed}, {result}");
                resultsPart2.Add(result);
            }
            var currentMin = resultsPart2.Min();
            Console.WriteLine($"[{seedStart}, {seedEnd}], {currentMin}");
            resultsPart2 = [currentMin];
        }
        Console.WriteLine($"Part 2 {resultsPart2}");

        /*
        BigInteger resultsPart2_smart = long.MaxValue << 32;
        for (int i = 0; i < seeds.Count; i += 2)
        {
            var seedStart = seeds[i];
            var seedLength = seeds[i + 1];
            var seedEnd = seedStart + seedLength - 1;
            var currentIntervals = almanac["seed"];

            string locationValue = seedStart;
            var currCategory = initialCategory;
            var currElem = initialValue;

            while (currCategory != finalCategory)
            {
                var nextCategory = categories[currCategory];

                foreach (var (start, end, dest_start, l) in almanac[currCategory])
                {
                    if (start <= currElem && currElem <= end)
                    {
                        currElem = dest_start + (currElem - start);
                        break;
                    }
                }
                currCategory = nextCategory;
                returnVal = currElem;
            }


            for (BigInteger seed = seedStart; seed <= seedEnd; seed++)
            {

                var result = SolveNaive(seed, startCategory, finalCategory, categories, almanac);
                // resultsPart1.Add(result);
                //Console.WriteLine($"{seed}, {result}");
                if (result < resultsPart2)
                {
                    resultsPart2 = result;
                }
            }
            Console.WriteLine($"[{seedStart}, {seedEnd}], {resultsPart2}");
        }
        Console.WriteLine($"Part 2 {resultsPart2}");
 
        for (int i = 0; i < seeds.Count; i += 2)
        {
            var seedStart = seeds[i];
            var seedLength = seeds[i + 1];
            var seedEnd = seedStart + seedLength - 1;

            var currentCategory = startCategory;

            var currentIntervals = almanac[currentCategory];

            var currNumber = seedStart;

        }
        */

        //Console.WriteLine(almanac.ToString());

        //Console.WriteLine(content.Length);
    }
}
