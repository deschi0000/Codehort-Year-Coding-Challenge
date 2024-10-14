# Variables
JAVAC = javac
JAVA = java
SRC = Main.java
TARGET = Main
INPUT = sample.tsv # Change to your file location
INPUT2 = fourchords.csv # Change to your file location
ARGS1 = -f1
ARGS2 = -f1 -d',' 
ARGS3 = -f1 -d',' head 
ARGS4 = -f1,3 

# Default target: compile and run
all: compile run

# Compile the Java code
compile:
	$(JAVAC) $(SRC)

# Run the compiled Java code
run:
	$(JAVA) $(TARGET) $(INPUT2) $(ARGS3)

# Clean up the class files (if needed)
clean:
	rm -f *.class
