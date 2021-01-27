import sys
import time
import threading

from RandomWordGenerator import RandomWord

shakespeare_file = "app/shakespeare.txt"
train_file = "train.txt"


def main(words_count, threads_count):
    # getAndCheckArguments()
    words = getWords(words_count)

    indexes = []
    if threads_count > 0:
        indexes = getRanges(len(words), threads_count)

    # if indexes is empty, it means no threads
    start = time.time()
    lookForWords(words, indexes)
    end = time.time()

    printSummery(start, end, len(indexes) > 0)


def getWords(count):
    rw = RandomWord(3,
                    constant_word_size=False,
                    include_digits=False,
                    special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                    include_special_chars=False)
    words = []
    while (True):
        if len(words) == count:
            break
        temp = rw.generate()

        if not temp in words:
            words.append(temp)

    return words


def getRanges(len_of_list, num_of_ranges):
    bunch_size = int(len_of_list / num_of_ranges)
    indexes = []
    for i in range(num_of_ranges):
        idx = (i + 1) * bunch_size - 1

        indexes.append(idx)

    return indexes


# return the ok array we build
# indicates which words appeared
def lookForWords(words: [str], indexes: [int]) -> None:
    using_threads = len(indexes) > 0
    if using_threads:
        lookForWordsUsingThreds(words, indexes)
    else:
        lookForWordsIterative(words)


def lookForWordsIterative(words):
    for word in words:
        checkSpecificWordInFile(word)


def lookForWordsUsingThreds(words, indexes):
    threads = []
    for i in range(len(indexes)):
        temp = threading.Thread(target=lookWithinRange, args=(words, indexes[0] + 1, i * indexes[0], i,))
        threads.append(temp)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def lookWithinRange(words, count, startIndex, thread_id):
    # print("args are -> ", words, count, startIndex, thread_id)

    words_to_check = words[startIndex:startIndex + count]
    print(f"thread {thread_id} with starting index {startIndex} had started, he has {count} to check")

    for word in words_to_check:
        # print(f"startIndex) {startIndex}checking word - {word}")
        checkSpecificWordInFile(word)

    print(f"thread {thread_id}  had finished")


def checkSpecificWordInFile(word_user: str) -> bool:
    with open(shakespeare_file, 'r') as file:
        txt = file.readline()

        while txt != '':
            txt_wards_array = txt.split()  # splitting wards by space, puts in array

            for word_text in txt_wards_array:
                if word_text == word_user:
                    file.close()
                    print(f"the ward) {word_user} is found")
                    return True

            txt = file.readline()

    return False


def printSummery(start: float, end: float, using_threads: bool):
    print("using threads %s" % str(using_threads))
    print("done in %s seconds " % str(end - start))


if __name__ == '__main__':
    main()
