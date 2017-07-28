from __future__ import print_function
import numpy as np


def findSimilar(iLike, userLikes):
    # Create an And similarity
    similarityAnd = userLikes * iLike
    similarityAndSum = similarityAnd.sum(axis=1)
    # Create an Or similarity
    similarityOr = userLikes + iLike
    userSimilarity = similarityAndSum / \
                     (similarityOr.sum(axis=1) - similarityAndSum)

    # Make sure they like something new
    while True:
        maxIndex = userSimilarity.argmax()
        newLikes = userLikes[maxIndex] - iLike
        newCount = len(newLikes[newLikes > 0])
        if newCount > 0:
            break
        else:
            # Zero that index out so it will find something else next time
            userSimilarity[maxIndex] = 0

    # Print the max similarity
    print("\nUser Similiarity: " + str(userSimilarity[maxIndex]))
    return maxIndex


def printMovie(id):
    print("    - " + str(id) + ": " + movieDict[id])


def processLikes(iLike):
    print("\n\nSince you like:")
    for like in iLike:
        printMovie(like)

    # Convert iLike into an array of 0's and 1's
    iLikeNp = np.zeros(maxMovie)
    for i in iLike:
        iLikeNp[i] = 1

    # Find the most similar user
    user = findSimilar(iLikeNp, userLikes)
    print("\nYou might like: ")
    # Find the indexes of the values that are ones
    # https://stackoverflow.com/a/17568803/3854385
    recLikes = np.argwhere(userLikes[user, :] == 1).flatten()

    for like in recLikes:
        # Don't reprint things the user has already said they like
        if iLikeNp[like] == 0:
            printMovie(like)


# Load Data
movieNames = np.loadtxt('./ml-100k/u.item', delimiter='|', usecols=(0, 1), \
                        dtype={'names': ('id', 'name'), 'formats': (np.int, 'S128')})
movieDict = dict(zip(movieNames['id'], movieNames['name']))

movieData = np.loadtxt('./ml-100k/u.data', delimiter='\t', usecols=(0, 1, 2), \
                       dtype={'names': ('user', 'movie', 'rating'), 'formats': (np.int, np.int, np.int)})
# print(movieNames)
# print(movieData)

# Compute average rating per movie
# This is non-ideal, pandas, scipy, or graphlib should be used here
movieRatingTemp = {}
for row in movieData:
    if row['movie'] not in movieRatingTemp:
        movieRatingTemp[row['movie']] = [row['rating']]
    else:
        movieRatingTemp[row['movie']].append(row['rating'])

movieRating = {}
movieRatingCount = {}

for key in movieRatingTemp:
    movieRating[key] = np.mean(movieRatingTemp[key])
    movieRatingCount[key] = len(movieRatingTemp[key])

# Get sorting ratings
# https://www.saltycrane.com/blog/2007/09/how-to-sort-python-dictionary-by-keys/
movieRatingS = sorted(movieRating.iteritems(), key=lambda (k, v): (v, k), reverse=True)

# Top 5 movies
print("Top Ten Movies:")
for i in range(0, 10):
    print(
        str(i + 1) + ". " + movieDict[movieRatingS[i][0]] + " (ID: " + str(movieRatingS[i][0]) + ") Rating: " + str(
            movieRatingS[i][1]) +
        " Count: " + str(movieRatingCount[movieRatingS[i][0]])
    )

print("\n\nTop Ten movies with at least 100 ratings:")
i = 0
printCount = 0
while printCount < 10:
    if movieRatingCount[movieRatingS[i][0]] >= 100:
        print(
            str(i + 1) + ". " + movieDict[movieRatingS[i][0]] +
            " (ID: " + str(movieRatingS[i][0]) + ") Rating: " +
            str(round(movieRatingS[i][1], 2)) +
            " Count: " + str(movieRatingCount[movieRatingS[i][0]])
        )
        printCount += 1
    i += 1

# Create a user likes numpy ndarray so we can use Jaccard Similarity
# A user "likes" a movie if they rated it a 4 or 5
# Create a numpy ndarray of zeros with demensions of max user id + 1 and max movie + 1 (because we'll use them as 1 indexed not zero indexed)
# print(movieData['user'].max())
maxMovie = movieData['movie'].max() + 1
userLikes = np.zeros((movieData['user'].max() + 1, maxMovie))
for row in movieData:
    if row['rating'] == 4 or row['rating'] == 5:
        userLikes[row['user'], row['movie']] = 1



while True:
    run = raw_input("\nWould you like to get a recommendation (Y/N) ")
    if len(run) == 0 or run[0] != 'Y':
        break
    iLike = []
    while True:
        movie = raw_input("Enter a movie ID that you like [1-" + str(maxMovie) + "]" +
                          " or leave blank if done: ")

        # Try to convert the entry to a number, set it to 0 if there is a value
        # error
        try:
            movieInt = int(movie)
        except ValueError:
            movieInt = 0

        if len(movie) == 0:
            break
        elif movieInt < 1 or movieInt > maxMovie:
            print("Invalid Selection")
            continue
        else:
            iLike.append(movieInt)
    if len(iLike) > 0:
        processLikes(iLike)
    else:
        print("You didn't enter any movies you like so we couldn't make any " +
              "suggestions!")