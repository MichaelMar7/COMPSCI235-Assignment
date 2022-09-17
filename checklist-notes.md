# Checklist and Notes

These are notes that I (mmar667) created to make it easier to plan out for the assignment. I'm not sure if we can submit this text file but I'll delete this file before the final commit if it's not allowed. Feel free to make changes to this file if you want to (only helpful changes).

### Lecture Slides
- **Flask and Jinja (Templates and Static folders)**: L11
- **Request Handling**: L12
- **Blueprints**: L12
- **Repository Pattern**: L13
- **Authentication**: L14 (L10 for HTTP stuff)
- **WTForms & Flask WTF**: L14 & L15
- **Testing**: L15 (L8 for intro)

### folder structure

Inside ***music*** folder
- **adapters (pre-set)** - contains the csvdatareader and its data. Also contains the repository pattern (abstract and memory repository), which connects to blueprints.
- **domainmodel (pre-set)** - objects (models) for the application (Don't think we need to do something with this)
- **templates (pre-set)** - contains html stuff
- **static** - contains css file
- **utilites** - contains utilite blueprint (amybe put in *blueprint* folder).
- **blueprint** folder(s) - blueprints and request handlers (may create multiple folders for each blueprint?)

 ***tests*** folder contains pytest stuff

### Repository Pattern

Maybe? Get lists and sets from csvdatareader and use them for the Repository class
Or the csvdatareader is Memory repository and be have to create the Abstract Repository class and add more methods in the repository.

Memory Repository
- Users
- All objects in domainmodel

### Blueprints

To get data into the webapp, we put them in the render_template() method (i.e. render_tempate( ... variable_name: variable or method, ...)) so they can be accessed in the templates.

## C requirements

Funcitonal Requirements
- [ ] Browsable tracks
    - Connect repository to template folder via request handling and stuff
    - Browser through list of tracks (previous and next tracks, maybe first and last tracks?)

Non-Funcional Requirements
- [x] Project Structure
    - folder structure from above
- [ ] User Interface - HTML, CSS & Jinja
    - Template and Static folder stuff
- [ ] Web Interface - HTTP
    - Request handlers in blueprints
- [x] Repository Pattern
- [ ] Unit and Integrated Testing
    - tests folder

## B requirements

Functional Requirements
- [ ] Displaying/searching tracks based on artists, genres, album etc. 
- [ ] Registering, logging in/logging out users
    - Authentication stuff
- [ ] Reviewing tracks
    - Use WTForms
    - In a tracks blueprint

Non-Funcitonal Requiements
- [ ] Use of Blueprints
- [ ] Use of authentication
- [ ] Use of HTML/WTForms

## A and A+ requirements

- [ ] The ***new cool feature!*** for **A**

- [ ] and a 2-3 page report of that feature for **A+**


### Web layout review notes

<!--
- Top Tracks and Album look different (Track horizontal, Albums vertical)?
    - For space for the main content block
    - Maybe put them on same bar?
- The links are alright. You can have a blueprint/page for Home, blueprint/page for Authentication, combining the register, login, and logout, a blueprint/page for browsing tracks and albums (maybe two blueprints for each). Since you have a liked tracks link, maybe we should have a profile page (that could be our *cool feature* if that counts) containing reviews and liked tracks.
    - So blueprint for Home, Tracks/Album Browsing (maybe two blueprints?), Authentication, Profile?
- Should be actually browser for album since that wasn't in the requirements?
- Needs a main content block
- Other than that, good job with the layout!

Yeah I reckon we should have browsable tracks and albums? 

-->
