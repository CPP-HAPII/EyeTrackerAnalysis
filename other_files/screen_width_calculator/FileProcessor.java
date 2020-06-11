import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.File;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.io.FileOutputStream;

import java.awt.Font;
import java.awt.font.FontRenderContext;
import java.awt.geom.AffineTransform;

public class FileProcessor {
    public static void main(String[] args) throws IOException {
        if(args.length == 0) {
            System.out.println("Please provide path to folder");
            return;
        } else if(args.length > 1) {
            System.out.println("Please provide only 1 folder");
            return;
        }

        List<String> results = new ArrayList<String>();
        File[] files = new File(args[0]).listFiles();
        Arrays.sort(files);
        for (File file : files) {
            if (file.isFile()) {
                results.add(file.getName());
                String fileContent = readFile(args[0]+file.getName());
                
                String outputFilename1 = args[0].substring(0, args[0].length() - 1) + "Output/" +file.getName();
                String outputFilename2 = args[0].substring(0, args[0].length() - 1) + "Output/" +file.getName() + ".html";

                //fileContent = fileContent.replace(" ", "");
                //fileContent = fileContent.replace(".", "");
                //fileContent = fileContent.replace(",", "");
                //fileContent = fileContent.replace("-", "");

                fileContent = fileContent.replace("\n", "");

                FileOutputStream out1 = new FileOutputStream(outputFilename1);
                FileOutputStream out2 = new FileOutputStream(outputFilename2);
                out1.write(fileContent.getBytes());
                out2.write(fileContent.getBytes());

                out1.close();
                out2.close();

                String text = fileContent;
                AffineTransform affinetransform = new AffineTransform();     
                FontRenderContext frc = new FontRenderContext(affinetransform,true,true);     
                Font font = new Font("Tahoma", Font.PLAIN, 12);
                int textwidth = (int)(font.getStringBounds(text, frc).getWidth());
                int textheight = (int)(font.getStringBounds(text, frc).getHeight());
                System.out.println(/*file.getName() + " Width: " +*/ textwidth);
                //System.out.println(file.getName() + " Height: " + textheight);
            }
        }
    }

    public static String readFile(String fileName) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(fileName));
        try {
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
    
            while (line != null) {
                sb.append(line);
                sb.append("\n");
                line = br.readLine();
            }
            return sb.toString();
        } finally {
            br.close();
        }
    }
}