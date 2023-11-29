# Julie-Your Personal Chatbot
## "Bringing Conversational Intelligence to Your Fingertips"

---

### Project Overview
Julie-Your Personal Chatbot is an interactive web-based chatbot designed to provide users with a unique and engaging conversational experience. This application allows users to interact with Julie, a virtual assistant, for various purposes including information retrieval, entertainment, and general conversation. Targeted towards users seeking a seamless and intuitive chatbot interface, Julie is also equipped with user authentication and profile management features, enhancing personalization and security.

---

### Features

#### User Authentication
- **Secure Login**: Robust login system with real-time validation and feedback.
- **AJAX-Driven Authentication**: Smooth and asynchronous user authentication process, enhancing the user experience without page reloads.

#### Profile Management
- **Personalized Experience**: Users can edit their profile information, including name, email, and bio.
- **Dynamic Profile Updates**: Real-time updates to user profiles with instant feedback.

#### UI Enhancements
- **Interactive Elements**: Elegant modal windows, button animations, and a responsive design.
- **Toast Notifications**: Informative toast messages for actions like profile updates or error information.

### Chatbot Interactivity 
- **Dynamic Interaction**: Julie, the chatbot, is programmed to interact dynamically with users. The JavaScript implementation in `script_chatbot.js` allows Julie to respond to user inputs in real-time, making the conversation flow naturally.
- **User Queries Handling**: The script handles various user queries, providing appropriate responses and guiding users through different functionalities of the application.

### Responsive User Interface Design
- **Adaptive Layout**: CSS files like `style_chatbot.css`, `style_login.css`, and `style_register.css` ensure that the application's layout adapts to different screen sizes and devices, providing an optimal viewing experience.
- **Aesthetic Appeal**: The CSS styling contributes to the aesthetic appeal of the application, with attention to color schemes, typography, and element positioning for a visually pleasing interface.

## Technologies Used
- **JavaScript**: For dynamic client-side scripting.
- **CSS**: For styling and responsive design.
- **HTML**: For structuring the web application.
- **Python (Django framework)**: For backend development.
- **SQLite and PostgreSQL**: For database management in development and production environments, respectively.
- **Git and GitHub**: For version control and source code management.
- **AJAX**: For asynchronous web requests.

## File Descriptions
- **`script_chatbot.js`**: Manages the chatbot's interactive features and user responses.
- **`script_login.js`**: Handles the login process, including client-side validation and feedback.
- **`script_register.js`**: Manages the registration process with input validation and AJAX requests for a smoother user experience.
- **CSS Files (`style_chatbot.css`, `style_login.css`, `style_register.css`)**: Provide styling for the chatbot, login, and registration pages, ensuring a responsive and attractive interface.

---

### Technical Details

#### AJAX-Driven Communication
- **Asynchronous Data Handling**: Uses AJAX for handling user authentication, registration, and profile management without page refresh.
- **Client-Server Interaction**: Efficient communication between the client and server, providing a seamless user experience.

#### JavaScript Enhancements
- **Dynamic Content Loading**: JavaScript functions to dynamically load and update user profile information.
- **Client-Side Validation**: Real-time form validation to ensure data integrity before submission.

---

## Setup and Deployment
1. **Local Setup**:
   - Clone the repository.
   - Set up a virtual environment and install dependencies.
   - Run the Django server locally for development and testing.

2. **Deployment on Heroku**:
   - Configure Heroku with necessary environment variables.
   - Deploy the application via Heroku Git or GitHub integration.

---

### Usage Instructions
1. **Registration**: New users can register using the registration form, providing essential details.
2. **Login**: Existing users can log in using their credentials to access the chat interface.
3. **Chatting with Julie**: Users can start conversing with Julie immediately after logging in.
4. **Editing Profile**: Users can update their profile information via the profile edit feature.

---

### User Account Management
- **Profile Creation and Customization**: Users can sign up and create their profiles with ease. The system allows for adding personal information like full name, email, and a unique username. Users can also customize their profiles by adding a bio, giving a personal touch to their interactions with Julie.
- **Profile Editing and Management**: A user-friendly interface empowers users to update their profile details at any time. This includes changing their email, modifying their bio, or updating their full name, ensuring that their interaction with Julie remains relevant and personalized.
- **Secure Profile Picture Upload**: Users have the option to upload a profile picture, enhancing their personalization experience. This feature uses Cloudinary for efficient and secure image storage and management, ensuring that user data is handled responsibly.
- **Account Deletion with Confirmation**: In line with best security practices, the application offers users the option to delete their accounts. This action requires a confirmation step to prevent accidental deletions, safeguarding user data against unintended loss.

### Chatbot Interactivity
- **Real-Time Chat with Julie**: The core feature of the application, users can interact with Julie in a chat interface that responds in real time. Julie is programmed to understand various user inputs, making the conversation flow naturally and engagingly.
- **Contextual Awareness and Memory**: Julie is not just a standard chatbot; it remembers past conversations with users. This memory feature allows Julie to provide contextual and continuous interactions, enhancing the user experience by making it feel more conversational and less transactional.
- **Smart Response System**: Julie's responses are not pre-scripted but are dynamically generated based on the user's input, making each conversation unique. This smart response system uses a combination of predefined rules and machine learning techniques to provide accurate and relevant responses.

### Notification System
- **Toast Notifications for Immediate Feedback**: The application employs an intuitive toast notification system. Whenever a user updates their profile, interacts with Julie, or performs any significant action within the application, they receive immediate feedback through these notifications. This feature enhances user engagement and provides clarity on the result of their actions.

### User Help and Support
- **Easy Access to Help and Support**: Understanding that users might need assistance, the application offers easy access to help and support. Users can inquire about functionalities, report issues, or seek help regarding their interaction with Julie, ensuring a supportive user experience.

### Customizable User Settings
- **User Preferences and Settings**: Users have the option to customize their interaction settings. This includes adjusting notification preferences, managing chat settings, or modifying other personal preferences, allowing them to tailor their experience to their liking.

### Advanced Chat Features
- **Multimedia Interaction**: Going beyond text, Julie can interact with users using multimedia elements like images and links, making the conversations more lively and informative.
- **Emotion Recognition**: Julie can recognize emotional cues in user messages and respond appropriately, adding a layer of emotional intelligence to the interactions.

### Functionality Testing

Functionality testing is a critical phase in the development of 'Julie - Your Personal Assistant'. This section ensures that every interactive element, such as buttons, forms, and the chat interface, operates as intended, providing a seamless and intuitive user experience.

#### Testing Interactive Elements
- **Profile Edit Button**: Located in the chatbot interface, this button allows users to access and modify their profile settings. A manual test involves clicking the button to ensure it opens the profile modal, allowing for data entry and submission.
- **Chat Input Field**: This field is a part of the chatbox where users interact with Julie. Testing involves entering various messages and verifying that Julie responds appropriately. The field should allow text input and clear out after message submission.
- **Toast Notification Trigger**: Toast notifications appear in response to user actions, like profile updates. Manual testing ensures that these notifications are triggered correctly and display the appropriate message.
- **Profile Update Form**: Inside the profile modal, users can update their information. Tests include entering new data into the form fields, submitting the form, and verifying that the profile is updated correctly. It also involves checking for form validations and error handling.
- **Account Deletion Process**: The account deletion feature is tested by initiating the deletion process and confirming that the account is removed only after user confirmation. This test also involves verifying that the process can be canceled without unintended consequences.

#### Simulated Manual Test Scenario
1. **Opening Profile Modal**: The tester clicks on the 'Profile' button to access the profile settings. The modal should open, displaying the current user's information.
2. **Editing Profile Information**: The tester modifies details like the full name, email, and bio. Each field is checked for input validation, ensuring that incorrect formats are flagged with an error message.
3. **Submitting Profile Changes**: After making changes, the 'Save changes' button is clicked. A successful submission should trigger a toast notification indicating that the profile has been updated.
4. **Verifying Profile Update**: The tester then reopens the profile modal to ensure that the changes have been saved and reflected correctly.
5. **Initiating Account Deletion**: The tester clicks on the 'Delete Profile' button and is prompted with a confirmation modal. The tester confirms deletion to proceed.
6. **Confirming Account Deletion**: Upon confirmation, the account should be deleted, and the user should be redirected to the login page. A failed deletion or incorrect redirection indicates a test failure.
7. **Chat Interaction Testing**: The tester interacts with Julie using the chat input field, sending various messages to assess Julie's response accuracy and relevance. The field's responsiveness and message display are also evaluated.

Through these manual tests, 'Julie - Your Personal Assistant' is rigorously evaluated to ensure that each element functions as expected, contributing to a reliable and user-friendly experience.

### Testing Different Pages and Elements

The testing process for 'Julie - Your Personal Assistant' is comprehensive, covering each page and its respective elements to ensure complete functionality and user satisfaction. Below is a detailed description of the testing procedures for different pages and elements, based on the structure outlined in the HTML files.

#### Testing the Chatbot Interface (chatbot.html)
- **Chatbox Functionality**: The chatbox is the main interface for user interaction with Julie. Tests include sending various types of messages and ensuring Julie's responses are timely and contextually relevant.
- **Username Display**: The top of the chatbox displays the user's username. Testing verifies that the correct username is displayed and updates immediately upon any changes.
- **Profile Modal**: Activated by the 'Profile' button, this modal allows users to view and edit their profile. Tests include opening the modal, editing fields, and verifying that changes are saved and reflected in the chat interface.
- **Message Input Validation**: Ensures that the message input field in the chatbox accepts text, clears after sending a message, and prohibits invalid inputs.

#### Testing the Login Page (login.html)
- **Form Submission**: Tests the login form for correct submission behavior, ensuring that valid credentials log the user in, while invalid credentials show appropriate error messages.
- **Input Fields**: Verifies that the username and password fields accept input, have proper validation, and display errors for invalid inputs.

#### Testing the Registration Page (register.html)
- **Account Creation**: Tests the account creation process, ensuring the form captures all necessary information and creates a new user account upon submission.
- **Validation Checks**: Ensures that all input fields, including email and password, are validated for correct format and completeness.

#### Testing Profile Management (Within chatbot.html)
- **Edit Profile Functionality**: Tests the ability to edit profile information such as name, email, phone number, and bio. Includes checks for input validation and proper data saving.
- **Profile Picture Upload**: Verifies the functionality of the profile picture upload feature, including image format restrictions and successful upload confirmation.
- **Account Deletion**: Confirms that the account deletion process works as intended, with appropriate warnings and confirmation steps to prevent accidental deletion.

#### Toast Notifications and Feedback (Within chatbot.html)
- **Notification Triggering**: Ensures that toast notifications are triggered by specific actions like profile updates or message sending.
- **Notification Content**: Confirms that notifications display correct information corresponding to the user's actions.

### Simulated Manual Testing for Each Page
A series of manual tests are conducted to simulate real-user scenarios, covering all aspects of the application:

1. **Login Page Testing**: A tester attempts to log in with various credentials, including incorrect and correct combinations, to verify proper handling of authentication.
2. **Registration Process**: The tester goes through the account creation process, filling in all required fields, and attempts to submit the form with both valid and invalid data.
3. **Chatbot Interaction**: Post-login, the tester engages with Julie, assessing the responsiveness, accuracy of responses, and overall user experience of the chatbot.
4. **Profile Editing and Viewing**: The tester accesses and modifies different aspects of their profile, checking for immediate updates and proper data handling.
5. **Toast Notifications**: During each interaction, the tester observes the triggering and content of toast notifications, ensuring they provide accurate and timely feedback.

Through these extensive testing procedures, 'Julie - Your Personal Assistant' is meticulously evaluated to ensure a flawless user experience across all its pages and functionalities.

### Manual Testing of JavaScript Functionalities

The JavaScript files of 'Julie - Your Personal Assistant' play a crucial role in enhancing the interactive aspects of the application. Manual testing of these files ensures that all dynamic features function as expected. Below are the details of the manual tests conducted on various JavaScript functionalities.

#### Testing script_chatbot.js
- **Edit Profile Functionality**: 
  - **Test**: Clicking the 'Edit' button next to profile fields should make the input fields editable.
  - **Result**: Successfully toggles the visibility of display and input elements for full name, email, phone number, and bio.
  
- **Profile Data Loading and Submission**:
  - **Test**: On opening the profile modal, existing user data should load correctly. Submitting the profile form should update user details.
  - **Result**: Data loading is accurate, and form submission updates the profile successfully with appropriate toast notifications.

- **Send Message Functionality**:
  - **Test**: Typing a message and clicking the send button or pressing enter should display the message in the chatbox.
  - **Result**: Messages are appended correctly to the chatbox, and the input field clears after sending.

- **Account Deletion Confirmation**:
  - **Test**: Clicking the 'Delete' button should prompt for confirmation. Confirming should delete the account.
  - **Result**: The confirmation modal appears correctly, and confirming deletes the user account and redirects to the login page.

#### Testing script_login.js
- **Login Form Submission**:
  - **Test**: Entering credentials and submitting the form should log the user in if credentials are correct.
  - **Result**: Form submission works as expected. Correct credentials log in the user, while incorrect ones show error messages.

#### Testing script_register.js
- **Registration Form Validation and Submission**:
  - **Test**: Filling out the registration form and submitting should create a new user account if the data is valid.
  - **Result**: The form captures all necessary information, validates input, and creates a new account upon correct data submission.

### Simulated Manual Testing for JavaScript Files
A series of manual tests are carried out for each JavaScript file to simulate real-world user interactions:

1. **Chatbot Script (script_chatbot.js) Testing**:
   - The tester engages with the chat interface, sending messages and observing Julie's responses for accuracy and timeliness.
   - The tester edits their profile, testing the functionality of each editable field and the responsiveness of the save changes button.
   - The account deletion process is tested to ensure it requires confirmation and correctly handles the deletion.

2. **Login Script (script_login.js) Testing**:
   - The tester attempts to log in with various credentials to assess the form's response to correct and incorrect data.

3. **Registration Script (script_register.js) Testing**:
   - The tester goes through the registration process, inputting data in each field, and attempts to submit the form with both valid and invalid data to test validations.

Through these manual tests, the JavaScript functionalities of 'Julie - Your Personal Assistant' are thoroughly evaluated, ensuring they contribute effectively to the application's interactivity and user experience.

### Manual Testing view:

<iframe src="https://scribehow.com/embed/Manual_Testing_for_Julie__Your_personal_assistant_website__0-f_FbrASw-XI4JwKOC6pA?as=scrollable&skipIntro=true" width="100%" height="640" allowfullscreen frameborder="0"></iframe>

### Lighthouse:
Mobile ![Lighthouse mobile](media/images/lighthouse%20mob.png)
Desktop ![Lighthouse desktop](media/images/lighthouse%20desk.png)

---
## Wireframes

### Mobile wireframes
![Login Page](media/images/Mobile-login%20page.png)
![Register Page](media/images/Mobile%20-%20Register%20page.png "Optional title")


### Desktop Wireframes
![Login Page](media/images/Desktop%20-%20Login%20page.png)
![Register Page](media/images/Desktop%20-%20Register%20page.png)

### Tablet Wireframes

![Login Page](media/images/ipad%20login.png)
![Register Page](media/images/iPad%20Pro%2012.9_%20-%202.png)

### Contributing
We welcome contributions from the community. Please refer to our contribution guidelines for more information on how to contribute effectively.
