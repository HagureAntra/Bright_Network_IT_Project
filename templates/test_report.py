"""
                                Testing 



Test Case	               Action Performed	            Expected Result	Actual Result	                            Pass/Fail

Home page loads	           Visit deployed URL	        Loads with styled interface	                        Page loads successfully	             Pass

Upload valid CSV	    Upload synthetic_logs.txt	    Results + flagged IPs displayed	                        Works as expected	             Pass

Upload invalid file	    Upload .docx or empty file	        Show error message	                                Catches error, displays error	 Pass

Download CSV	        Click download button	            CSV file downloaded	                                        Works	                 Pass

Responsive design	       Resize or use phone	               Layout adjusts	                                Looks good on mobile	         Pass



                                    Summary

During testing, I verified that the deployed Flask application correctly handles synthetic log uploads and successfully identifies suspicious IP addresses based on frequency and user agent patterns. The homepage rendered properly with dark-mode styling and functional buttons. Uploading a valid CSV resulted in accurate detection and downloadable flagged IPs. Error handling worked when uploading broken files — confirming the app’s robustness. Minor delays were noted on first load due to free-tier Render cold start, which is expected.
Additional features such as IP geolocation and visual bar charts functioned correctly. Mobile responsiveness was confirmed. Overall, the system performed as expected and can serve as a practical low-cost tool for basic bot detection, suitable for small media startups.




"""