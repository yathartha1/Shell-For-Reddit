# Shell-For-Reddit

Shell For Reddit is a linux shell emulator written in Python that lets you browse reddit via command line.
It is available for macOS.

## Steps to Run the Application
* Download the dmg file located in the Application folder
* Open the dmg file
* Copy the Shell-For-Reddit application into your Applications Folder
* Run the application

**Features**

* Browse public subreddits, posts, comments, and users.
* Iterate through comments and post indexes.
* Search for posts, comments, and users.
* Clear all the commands on the screen.
* Iterate through old commands using up/down keyboard press.

**Example Commands**

* `# ls` - list posts from the frontpage
* `# ls funny` - lists posts from /r/funny
* `# ls subreddits` - lists a list of subreddits
* `# view comments 3` - views comments for the specified post index
* `# view more comments` - load more comments for current post scope

## Commands

* **ls**
  * Options:
    * **[hot|new|rising|top|controversial]** - sort the list based on categories
    * **[next|previous]** - can only be used on result set
    * **[subreddit] [next|previous]** - can only be used on result set
 * Description: list posts from the the specified subreddit or the front page if no subreddit specified and sorts by optional hot(default), new, rising, top, controversial.
* **ls subreddits**
  * Options:
    * **[next|previous]** - can only be used on result set
  * Description: list all public subreddits available on reddit
* **view**
  * Options:
    * **[index]** - can only be used on result set
  * Description: opens the permalink of the specified post index in a browser window.
* **view comments**
  * Options:
    * **[index]** - can only be used on result set
  * Description: loads the comments of the specified post index.
* **view more comments**
  * Description: Loads more comments from the post scope if there are posts to load.
* **search**
  * Options:
    * **[search term]**
    * **ls [next|previous]** - can only be used on result set
  * Description: Searches reddit for the specified search term.
* **clear**
  * Description: Clears the screen
* **exit**
  * Description: Exits the application

## Libraries Used

- [Praw](https://github.com/praw-dev/praw)
- [Kivy](https://github.com/kivy/kivy)
