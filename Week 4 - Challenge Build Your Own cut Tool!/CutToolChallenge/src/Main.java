import java.io.*;
import java.util.LinkedList;
import java.util.Queue;

public class Main {
    public static void main(String[] args) {
        Integer headTailLength = 5;
        String columnArgument = "";
        String fileName = "";
        String delimiter = null;
        Integer fieldValue = null;
        Boolean tail = false;
        Boolean head = false;
        String[] fieldValueArgs = null;
        Integer lowerFieldValue = null;
        Integer higherFieldValue = null;
        Boolean stdInput = false;

        // Extract the args
        if (args.length < 1) {
            System.err.println("Error: Please enter a file");
            return;
        } else {
            for (String arg : args) {
                // Debug print to stderr
                //System.err.println("arg: " + arg);

                // Get the file
                if (arg.contains(".csv") || arg.contains(".tsv")) {
                    fileName = arg;
                }

                // Check for field/column argument
                if (arg.startsWith("-f")) {
                    columnArgument = arg.replace("-f", "").trim();
                    if (!columnArgument.isEmpty()) {
                        try {
                            if (columnArgument.contains(",") || columnArgument.contains(" ")) {
                                fieldValueArgs = columnArgument.split("[, ]");
                                if (Integer.parseInt(fieldValueArgs[0]) < 0 || Integer.parseInt(fieldValueArgs[1]) < 0) {
                                    System.err.println("Field value argument cannot be below 0");
                                    return;
                                } else {
                                    lowerFieldValue = Integer.parseInt(fieldValueArgs[0]);
                                    higherFieldValue = Integer.parseInt(fieldValueArgs[1]);
                                }
                            } else {
                                fieldValue = Integer.parseInt(columnArgument);
                                if (fieldValue < 0) {
                                    System.err.println("Field value argument cannot be below 0");
                                    return;
                                }
                            }
                        } catch (NumberFormatException e) {
                            System.err.println("Error: Please specify a valid integer for the column selection");
                            return;
                        }
                    }
                }

                // Check for delimiter argument
                if (arg.startsWith("-d")) {
                    delimiter = arg.replace("-d", "").trim();
                }

                // Check if head or tail
                if (arg.equals("tail")) {
                    tail = true;
                }

                if (arg.equals("head")) {
                    head = true;
                }
            }
        }

        // Set default delimiter if not provided
        if (delimiter == null) {
            if (fileName.endsWith(".csv")) {
                delimiter = ",";
            } else if (fileName.endsWith(".tsv")) {
                delimiter = "\t";
            } else {
                System.err.println("Error: Invalid file type");
                return;
            }
        }

//        System.err.println("Delimiter: " + delimiter);
//        System.err.println("File with Path: " + fileName);

        // BufferedReader setup
        BufferedReader br;
        try {
            if (fileName.isEmpty() || fileName.equals("-")) {
                br = new BufferedReader(new InputStreamReader(System.in));
                stdInput = true;
            } else {
                br = new BufferedReader(new FileReader(fileName));
            }
        } catch (FileNotFoundException e) {
            System.err.printf("Error: The file at path %s was not found. Please check if the file exists.\n", fileName);
            return;
        }

        // Process the file or standard input
        try (br) {
            String line;
            int currentLine = 0;
            Queue<String> tailQueue = new LinkedList<>();

            while ((line = br.readLine()) != null) {
                currentLine++;

                // Head case: Print first N lines and exit early
                if (head && currentLine <= headTailLength) {
                    printLine(line, delimiter, fieldValue, lowerFieldValue, higherFieldValue);
                }

                // Tail case: Keep last N lines in a queue
                if (tail) {
                    tailQueue.add(line);
                    if (tailQueue.size() > headTailLength) {
                        tailQueue.poll(); // Maintain queue size
                    }
                }

                // General case: Neither head nor tail
                if (!head && !tail) {
                    printLine(line, delimiter, fieldValue, lowerFieldValue, higherFieldValue);
                }
            }

            // Print tail if necessary
            if (tail) {
                for (String tailLine : tailQueue) {
                    printLine(tailLine, delimiter, fieldValue, lowerFieldValue, higherFieldValue);
                }
            }

        } catch (IOException e) {
            System.err.println("Error: An I/O error occurred while reading.");
        }
    }

    // Function to print the line with the correct field values
    private static void printLine(String line, String delimiter, Integer fieldValue, Integer lowerFieldValue, Integer higherFieldValue) {
        String[] values = line.split(delimiter);
        if (fieldValue != null) {
            if (fieldValue <= values.length) {
                System.out.println(values[fieldValue - 1]);
            }
        } else if (lowerFieldValue != null && higherFieldValue != null) {
            if (higherFieldValue > values.length) {
                System.err.println("Error: Column doesn't exist in the file");
                return;
            }
            for (int i = lowerFieldValue - 1; i < higherFieldValue; i++) {
                System.out.printf("%s%s", values[i], (i < higherFieldValue - 1) ? delimiter : "\n");
            }
        } else {
            System.out.println(String.join(delimiter, values));
        }
    }
}
