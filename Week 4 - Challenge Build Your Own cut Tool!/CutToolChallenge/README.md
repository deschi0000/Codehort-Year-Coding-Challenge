

# Week 4 Challenge: Build Your Own cut Tool!

This week is another dive into Unix command-line tools, by building our own version of ```cut```




This challenge helped to advance my skills by way of:
- Learning about Unix philosophy and command-line tool design
- Practicing file I/O and string manipulation
- Gaining experience in building practical, usable software tools


## These Features will be implemented:

### Step 0: Setup

This week we will develop using Java and test in a Unix enivronment to make sure our pipes, etc work.

We will need:

- JDK (for compiling and running outside of our editor)
- IntelliJ / Eclipse

If not running on Linux:

- Git Bash
- MinGW (used for running the make file if you wish to use it for debugging and ease) https://sourceforge.net/projects/mingw/ Make sure that the path to the bin folder is included in the enivronment variables.




### Step 1: Basic Functionality
Implement a simple version of cut that can:
- Open a tab-separated file
- Print out the second field (-f2) from each line


   ```bash 
    $ java Main -f2 sample.tsv
    f1
    1
    6
    11
    16
    21
   ```


### Step 2: Custom Delimiters
Add support for the -d option to specify custom delimiters

   ```bash 
     $ java Main -f1 -d, fourchords.csv | head -n5
    ?Song title
    "10000 Reasons (Bless the Lord)"
    "20 Good Reasons"
    "Adore You"
    "Africa"
   ```


### Step 3: Multiple Fields
Support the -f option for specifying multiple fields

   ```bash 
    $ java Main -f1,2 sample.tsv
    f0      f1
    0       1
    5       6
    10      11
    15      16
    20      21
    
    $ java Main -d, -f"1 2" fourchords.csv | head -n5
    ?Song title,Artist
    "10000 Reasons (Bless the Lord)",Matt Redman and Jonas Myrin
    "20 Good Reasons",Thirsty Merc
    "Adore You",Harry Styles
    "Africa",Toto
   ```


### Step 4: Standard Input
Support reading from standard input when no filename is provided or ```-``` is used:

   ```bash 
    $ tail -n5 fourchords.csv | java Main -d, -f"1 2"
    "Young Volcanoes",Fall Out Boy
    "You Found Me",The Fray
    "You'll Think Of Me",Keith Urban
    "You're Not Sorry",Taylor Swift
    "Zombie",The Cranberries
   ```

### Step 5: Integration
Combine the cut tool with other Unix commands to count unique artists:
   ```bash 
  $ java Main -f2 -d, fourchords.csv | uniq | wc -l
  155
   ```

### Considerations this week
- Optimization for larger files by using a Queue
- More effort put into error handling

## Exectuable Artifact

This project can be turned into an executable in the following way:
### Step 1: Complie your project
   ```bash 
  javac Main.java
   ```

### Step 2: Create a Manifest File ```manifest.txt``` 
Contaning the following:
   ```bash 
  Manifest-Version: 1.0
Main-Class: Main
   ```

### Step 3: Package the Executable JAR
Run the following command:
   ```bash 
  jar cfm MyCutTool.jar manifest.txt Main.class
   ```

This command does the following:

- ```c``` = create a new archive
- ```f``` = specify the output file (```MyCutTool.jar```)
- ```m``` = include the manifest file (```manifest.txt```)

You can now run the JAR file
   ```bash 
  java -jar MyCutTool.jar
   ```


### Step 4: Run from anywhere
Create a new directory.
   ```bash 
  C:\Tools
   ```

- Place the jar file within.
- Add this path to your Systems Path Variable.
- Create a bat file ```MyCutTool.bat```
- The contents of this bat file:  
  ```bash
  @echo off
  java -jar "C:\Tool\MyCutTool.jar" %*
  ```
  (This .bat file can be placed in any folder whose path is listed in system variable, 
the main point is that in the file, it points to the where the jar file is)

```MyCutTool``` can now be used anywhere: 
```bash
    C:\Users\Dave>MyCutTool C:\Tools\fourchords.csv -f1,2 head
    ?Song title,Artist
    "10000 Reasons (Bless the Lord)",Matt Redman and Jonas Myrin
    "20 Good Reasons",Thirsty Merc
    "Adore You",Harry Styles
    "Africa",Toto
  ```
