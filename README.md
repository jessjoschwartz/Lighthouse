Lighthouse
==========

## About Lighthouse
Lighthouse is Lyft for walking. It’s designed to give people peace of mind when making brief trips -- trips now made by taxi to avoid the unease of walking alone in unsafe areas or after dark. Ultimately, the mission of Lighthouse is to fill a gap in current public and private transportation services and create safer, more friendly communities.

## How Lighthouse Works
When a user (“traveler”) wants to walk a short distance with someone else, he/she initiates a request via Lighthouse. Geolocation determines the current location and the user enters the destination and Google Places Autocomplete allows the destination field to accepts place names in case a user does not know the street address. The database records the request, which is then queried for the Available Trips page and shows the traveler’s current address, destination address, and first name. When a guide clicks on the trip request, he/she see the map that visualizes the current location and destination. 

From the time a guide accepts a request until he/she confirms the trip is complete, the status of the journey is updated for both parties using AJAX polling. During the journey, ten state changes occur (see outline of changes here). At the start of the project, I studied apps like Lyft and Uber to understand the state changes and how they inform a passenger’s experience (see initial wireframes here). I also met with a Lyft engineer to learn more about the driver-side of the app and how this informs the user experience for both the driver and passenger. As a community manager, I’ve listened to a lot of feedback about product design, so it was important to me to make the state change process as streamlined as possible. I achieved this via polling and using ajax to make the page components modular. 

## Database Schema
My SQLAlchemy database has three tables: users, trips, and statuses. All users table data records information from the sign-up form. Data records in the trips table in the database when the traveler requests a trip. It extracts the latitudes and longitudes for the current location and destination and the corresponding physical addresses from Google Maps and IDs of the traveler and guide. The statuses table records the progress of the trip in three phases via datetime: accepted, confirmed, and completed.


## Next Steps

**App functionality**
- Build for mobile: Because Lighthouse is intended to be used on the go, it should be rebuilt for iOS or Android.
- Profile and settings: Information about the guide and traveler should be displayed within the interface once a trip has been accepted. Additionally, the app also needs a profile management page, payment page, and help page.
- Guide and traveler modes: Guide and traveler modes should be visible in the interface and allow users to toggle between them. Additionally, access to guide pages should be restricted so only guides can see these pages. 
- Guide compensation: To streamline payment, it should be automated at the end of the trip. 
- Real-time updates: Currently, Lighthouse uses polling to update the request sequence. For a better user experience, I would replace polling with SocketIO. I would also add guide ETA and real-time map tracking.
- Automated communications: Travelers should be clearly alerted when his or her guide has arrived. Twilio could be implemented to text a traveler.
- Cancellation: Both guides and travelers should have the option to cancel trips without penalty within five minutes of requesting or accepting and doing so should notify the other party.
- Guide availability: Because Lighthouse is first and foremost an app intended to ensure physical safety, the app should provide messaging if all guides are available. It should also provide a link for private and public services (taxis, Lyft, Uber) to ensure users immediately have an alternate transportation option.

**Maps-based features**
- Distance minimums and caps: Lighthouse is intended for short distances of .25 to 2 miles. Lighthouse should calculate distances based on calculating route length from the Google Maps API and reject trips that are outside of the specified range. 
- Suggest safest route: When a trip has been confirmed, the app should provide the safest suggested walking route using information from the Crimespotting API.
- Proximity: Lighthouse currently posts all available trips to guides. Ideally, it should post trips within half a mile of a guide. Proximity can be detected via setting bounding boxes in the Google Maps API. Additionally, Lighthouse could also post trips that are directionally similar to a guide’s destination so a guide can choose more convenient trips.
Communication and messaging

**Social elements**
- User delight: When riding in a car, silence is socially acceptable. While walking, it’s potentially more awkward. To ensure a comfortable, friendly experience, Lighthouse should provide a page of fun conversation prompts.
- Ratings system: A ratings system should be implemented for both guides and travelers to incentivize positive, friendly behavior. Ratings should be visible to both parties: to guides when they are selecting trips and travelers when they have receive confirmation that their trip has been accepted.
- Invite social network: “Who are the guides and how do you ensure they are safe?” is the the most common question I’ve received about Lighthouse. Like Lyft and Uber, Lighthouse would have a rigorous application process and include background checks. Concerning recruitment, I think it would be interesting to target people with quantified self devices like UP24 and Fitbit because they would perceive Lighthouse as being a mutually beneficial service: they get more exercise and in doing so, help someone else.

## Technologies Used
1. Python/HTML/CSS/jQuery/Javascript/AJAX
2. Flask
3. SQLAlchemy
4. Google Maps Javascript API V3


