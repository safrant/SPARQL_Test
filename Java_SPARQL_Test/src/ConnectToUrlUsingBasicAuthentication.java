/*****************************************************************/
/* Copyright 2013 Code Strategies                                */
/* This code may be freely used and distributed in any project.  */
/* However, please do not remove this credit if you publish this */
/* code in paper or electronic form, such as on a web site.      */
/*****************************************************************/


import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

import org.apache.commons.codec.binary.Base64;

public class ConnectToUrlUsingBasicAuthentication {

	public void run() {

		try {
			String webPage = "http://192.168.1.1";

			String query = "select%20(%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23Type_Code%3E%20as%20%3Fs)%20%3Fp%20%3Fo%20%3Fg%20%7B%20%0A%20%20%7B%20%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23Type_Code%3E%20%3Fp%20%3Fo%20%7D%20%0Aunion%20%0A%20%20%7B%20graph%20%3Fg%20%7B%20%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23Type_Code%3E%20%3Fp%20%3Fo%20%7D%20%7D%20%0A%7D";
			String STARDOG = "https://ncias-p793-v.nci.nih.gov/NCIEVS/query?query=";
			webPage = STARDOG;
			String name = "NA";
			String password = "NA";

			String authString = name + ":" + password;
			System.out.println("auth string: " + authString);
			byte[] authEncBytes = Base64.encodeBase64(authString.getBytes());
			String authStringEnc = new String(authEncBytes);
			System.out.println("Base64 encoded auth string: " + authStringEnc);

			URL url = new URL(webPage);
			URLConnection urlConnection = url.openConnection();

			String acceptFormat = "application/sparql-results+json";


			urlConnection.setRequestProperty("Accept", acceptFormat);

			urlConnection.setRequestProperty("Authorization", "Basic " + authStringEnc);
			InputStream is = urlConnection.getInputStream();
			InputStreamReader isr = new InputStreamReader(is);

			int numCharsRead;
			char[] charArray = new char[1024];
			StringBuffer sb = new StringBuffer();
			while ((numCharsRead = isr.read(charArray)) > 0) {
				sb.append(charArray, 0, numCharsRead);
			}
			String result = sb.toString();
			System.out.println(result);
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}


	public static void main(String[] args) {

		try {
             new ConnectToUrlUsingBasicAuthentication().run();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}

