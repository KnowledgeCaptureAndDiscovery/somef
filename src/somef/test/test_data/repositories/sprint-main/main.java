package tr.com.srdc.xsd2owl;


import java.io.File;
import java.io.FileOutputStream;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.Level;


public class main {

	private Logger logger = LoggerFactory.getLogger(this.getClass());
	public static void main(String[] args) {
		main(args, System.getProperty("user.dir"));
	}
	public static void main(String[] args, String basePath) {
		Options options = new Options();
		Option xsdfileOption = Option.builder("x")
				.longOpt("xsd")
				.hasArg()
				.desc("path to XSD File (default: stdout)")
				.build();
		Option outputfileOption = Option.builder("o")
				.longOpt("outputfile")
				.hasArg()
				.desc("path to output file in OWL Format (default: stdout)")
				.build();
		Option helpOption = Option.builder("h")
				.longOpt("help")
				.desc("show help info")
				.build();
		Option verboseOption = Option.builder("v")
				.longOpt("verbose")
				.desc("show debugging output")
				.build();
		options.addOption(xsdfileOption);
		options.addOption(outputfileOption);
		options.addOption(helpOption);
		options.addOption(verboseOption);

		CommandLineParser parser = new DefaultParser();
		try {
			CommandLine lineArgs = parser.parse(options, args);

			String[] mOptionValue = getOptionValues(xsdfileOption, lineArgs);
			if (checkOptionPresence(verboseOption, lineArgs)) {
				setLoggerLevel(Level.DEBUG);
			} else {
				setLoggerLevel(Level.ERROR);
			}

			if (mOptionValue == null) {
				printHelp(options);
			} else {
				String file="";
				String outputfile = "";
				if(lineArgs.hasOption("x")) {
					file =System.getProperty("user.dir")+File.separator+lineArgs.getOptionValue("x");
				}
				if(lineArgs.hasOption("o")) {
					outputfile =System.getProperty("user.dir")+File.separator+lineArgs.getOptionValue("o");
				}else {
					outputfile =System.getProperty("user.dir")+File.separator+"output.rdf";
				}
				
				long startTime = System.currentTimeMillis();
				XSD2OWLMapper mapping = new XSD2OWLMapper(new File(file));

				mapping.setObjectPropPrefix("");
				mapping.setDataTypePropPrefix("");
				mapping.convertXSD2OWL();
				FileOutputStream ont;

				try {
					//File f = new File(basePath+File.separator+"output"+File.separator+"netex_facility_support.rdf");
					File f = new File(outputfile);
					f.getParentFile().mkdirs();
					ont = new FileOutputStream(f);
					mapping.writeOntology(ont, "RDF/XML");
					ont.close();
					long endTime = System.currentTimeMillis() - startTime;
					System.out.println("AUTOMATIC GENERATION OF ONTOLOGIES FROM NON-ONTOLOGICAL SOURCES");
					System.out.println("Time "+endTime+" ms");
					System.out.println("------Process DONE------");
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}catch(Exception e){
			e.printStackTrace();
			System.out.println("Error : " + e.getMessage());
			System.out.println("Process FAILED------");
		}


	}
	private static String[] getOptionValues(Option option, CommandLine lineArgs) {
		if (lineArgs.hasOption(option.getOpt())) {
			return lineArgs.getOptionValues(option.getOpt());
		}else {
			return null;
		}
	}
	private static void printHelp(Options options) {
		HelpFormatter formatter = new HelpFormatter();
		formatter.printHelp("java -jar xsd2owl.jar <options>\noptions:", options);
	}
	private static boolean checkOptionPresence(Option option, CommandLine lineArgs) {
		return lineArgs.hasOption(option.getOpt());
	}
    private static void setLoggerLevel(Level level) {
        Logger root = LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
        ((ch.qos.logback.classic.Logger) root).setLevel(level);
    }

}
