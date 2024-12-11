Instructions/Guide:

This project is a social media site where users can upload, visualize, and share their music listening history.
Spotify allows users to download JSON a file containing their listening history from their website. When downloaded, users are given files like this one here:
[
    {
    "endTime" : "2023-12-31 00:45",
    "artistName" : "The Beatles",
    "trackName" : "Help! - Remastered 2009",
    "msPlayed" : 139560
  },
    {
    "endTime" : "2023-12-31 17:02",
    "artistName" : "The Beatles",
    "trackName" : "Now And Then",
    "msPlayed" : 248333
  }
]

After users have created an account, these files can be uploaded on their profile to share their listening history, see others' listening history, create and share playlists, and see a database of songs. This application assumes that songs uploaded by the users already correspond to Song objects saved in Django's database. I've included a sample data file that can be uploaded, sampleData.json, if someone wants to create a new account and test data uploads.