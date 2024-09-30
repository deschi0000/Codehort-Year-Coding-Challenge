
# Week 1: Build Your Own wc Tool!

My own version of the classic Unix command-line tool wc.

### Step 1-5: Implement These Features 🏗
- Step 1: ```-c``` option: Count bytes in a file 
   ```bash 
   > python new-wc -c test.txt 342190 test.txt
   ```
- Step 2: ```-l``` option: Count lines in a file 
   ```bash
   > python new-wc.py -l test.txt
      7145 test.txt
   ```

- Step 3: ```-w``` option: Count words in a file  
   ```bash 
   > python new-wc.py -w test.txt
   58164 test.txt
   ```

- Step 4: ```-m``` option: Count characters in a file 
   ```bash 
   > python new-wc.py -m test.txt 
   339292 test.txt
   ```

- Step 5: Default behavior: Combine ```-c```, ```-l```, and ```-w``` 
   ```bash 
   > python new-wc.py test.txt
      7145   58164  342190 test.txt
   ```

### Final Boss Step: Level Up! 🔥

The tool reads from standard input if no filename is given.
   ```bash
   >cat test.txt | python new-wc.py -l
    7145
   ```





## Tech

Python


