import java.awt.*;
import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;

// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
public class Main {
    public static void main(String[] args) {

        Integer headTailLength = 5;

        String columnArgument = "";
        String fileName = "";

        String delimeter = null;
        Integer fieldValue = null;

        Boolean tail = false;
        Boolean head = false;

        String fieldValueArgs[] = null;
        Integer lowerFieldValue = null;
        Integer higherFieldValue = null;

        for (String arg : args) {
            System.out.println("arg: " + arg);
        }

//        Extract the args
        if (args.length < 1) {
            System.out.println("Error: Please enter a file");
        } else  {
            for (String arg : args) {
                // Get the file
                if (arg.contains(".csv") || arg.contains(".tsv")){
                    fileName = arg;
                }

                // Check for field/column argument
                if (arg.contains("-f")){
                    columnArgument = arg.replace("-f","").trim();
                    if (!columnArgument.isEmpty()){
                        try {
                            // See if there is a range of columns
                            if (columnArgument.contains(",") || columnArgument.contains(" ")){
                                if (columnArgument.contains(",")){
                                    fieldValueArgs = columnArgument.split(",");
                                }
                                else if (columnArgument.contains(" ")){
                                    fieldValueArgs = columnArgument.split(" ");
                                }
//                                for (String i : fieldValueArgs){
//                                    System.out.println(i);
//                                }
                                // Make sure that both arguments are valid fields
                                if (Integer.parseInt(fieldValueArgs[0]) < 0 || Integer.parseInt(fieldValueArgs[1]) < 0){
                                    System.out.println("Field value argument cannot be below 0");
                                    throw new NumberFormatException();
                                } else {
                                    lowerFieldValue = Integer.parseInt(fieldValueArgs[0]);
                                }
                            }
                            // If only one value, set the fieldValue
                            else {
                                fieldValue = Integer.parseInt(columnArgument);
                                if (fieldValue < 0) {
                                    System.out.println("Field value argument cannot be below 0");
                                    throw new NumberFormatException();
                                }
                                System.out.println("Field Value: " + fieldValue + "\n");
                            }
                        } catch(NumberFormatException e){
                            System.out.println("Error: Please specify a valid integer for the column selection");
                            throw new NumberFormatException();
                        }
                    }
                }
                // Check for  delimeter argument
                if (arg.contains("-d")){
                    delimeter = arg.replace("-d", "").trim();
                }
                // Check to see if head and tail constraints are in effects
                if (arg.trim().contains("tail")) {
                    tail = true;
                    System.out.println(arg.trim().contains("tail"));
                }

                if (arg.trim().contains("head")) {
                    head = true;
                    System.out.println(arg.trim().contains("head"));
                }
            }
        }

        // Check to see what the delimeter will be
        if (delimeter == null) {
            if (fileName.endsWith(".csv")) {
                delimeter = ",";
            } else if (fileName.endsWith(".tsv")) {
                delimeter = "\t";
            } else {
                System.out.printf("Error: Invalid file type");
                return;
            }
        }

        System.out.println("Delimeter: " + delimeter);
        System.out.println("\nFile with Path: " + fileName);


        BufferedReader br;

        if (fileName.isEmpty()) {
//            if (fileName.isEmpty() || fileName.equals("-")) {
            br = new BufferedReader(new InputStreamReader(System.in));
            System.out.println("Reading from standard input. Press Ctrl+D (or Ctrl+Z on Windows) to end input.");
        } else {
            try {
                br = new BufferedReader(new FileReader(fileName));
            } catch (FileNotFoundException e) {
                System.out.printf("Error: The file at path %s was not found. Please check if the file exists.\n", fileName);
                return;
            }
        }



        try (br) {
//            try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            int currentLine = 0;
            long totalLinesInFile = br.lines().count();
            br.close(); // Close and re-open for actual reading

            // Read the file with a buffered reader
            try (BufferedReader br2 = new BufferedReader(new FileReader(fileName))) {

                int tailStart = (int) (tail ? totalLinesInFile - headTailLength : 0); // ie 95-5 == 90 will start point

                while ((line = br2.readLine()) != null) {
                    currentLine ++;
                    if (tail && currentLine < tailStart) continue; // skip until the last five values are reached
                    if (head && currentLine > headTailLength) break; // We break after the first five values

                    Boolean ValidFieldValue;

                    // Check to see if the lines have to be skipped if only reading the last five values

                    String[] values = line.split(delimeter);
//                    currentLine++;

                    if (values.length < 2) {
                        System.out.println("Please specify a valid delimeter");
                        return;
                    }

                    // Check to see if the field value is valid
                    if (fieldValue != null) {
                        if (fieldValue > values.length) {
                            System.out.println("Error: Column doesn't exist in the file");
                            throw new IndexOutOfBoundsException();
                        }
                    }

                    if (higherFieldValue == null && fieldValueArgs != null) {
                        higherFieldValue = Integer.parseInt(fieldValueArgs[1]);
                        if (higherFieldValue > values.length) {
                            System.out.println("Error: Column doesn't exist in the file");
                            throw new IndexOutOfBoundsException();
                        }
                    }

                    // If no field value / column given, business as usual
                    if ((fieldValue == null) && (lowerFieldValue != null) && (higherFieldValue != null)) {
                        for (int i = 0; i < values.length; i++) {
                            // Don't print the last delimeter
                            if (i >= lowerFieldValue && i < higherFieldValue) {
                                System.out.printf("%s%s", values[i-1], delimeter);
                            }
                            else if (i == higherFieldValue) {
                                System.out.printf("%s", values[i-1]);
                            }
                        }
                        System.out.println();
                    } else if (fieldValue != null) {
                        for (int i = 0; i < values.length; i++) {
                            if (i == fieldValue) {
                                System.out.println(values[i - 1]);
                            }
                        }
                    } else if (fieldValue == null) {
                        for (int i = 0; i < values.length; i++) {
                            if (i < (values.length - 1)){
                                System.out.printf("%s%s", values[i], delimeter);
                            }
                            else {
                                System.out.printf("%s", values[i]);
                            }
                        }
                        System.out.println();
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.out.printf("Error: The file at path %s was not found. Please check if the file exists.\n", fileName);

        } catch (IOException e) {
            System.out.printf("Error: An I/O error occurred while reading the file at path %s. Please try again.\n", fileName);
        }
    }
}

    //        'C:\Users\Dave\Documents\Coding\Week 4 - Java\CutToolChallenge\testdata\fourchords.csv'
//        'C:\Users\Dave\Documents\Coding\Week 4 - Java\CutToolChallenge\testdata\sample.tsv'

    //        Get the Current Directory and the file for the path for processing.
//    String currentDir = System.getProperty("user.dir");
//        Path projectRoot = Paths.get("").toAbsolutePath();
//        System.out.println("currnet dir: " + currentDir);

//        Path fileName = Paths.get(currentDir.toString(), "testdata", "fourchords.csv");
//        Path csvFile = Paths.get(projectRoot.toString(), "testdata", "fourchords.csv");

//        Debug with the IntelliJ run
//        Path pathFileName = Paths.get(currentDir.toString(), "testdata", "fourchords.csv");
//        Path pathFileName = Paths.get(currentDir.toString(), "testdata", "sample.tsv");
//        fileName = pathFileName.toString();
