import sys
import time
import threading

from RandomWordGenerator import RandomWord

shakespeare_file = "app/shakespeare.txt"
train_file = "train.txt"
TOTAL = 0


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


def getFileAsText(file_text):
    file = open(file_text, mode='r')
    all_of_it = file.read()
    file.close()

    return all_of_it


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
    file_text = getFileAsText(shakespeare_file)
    using_threads = len(indexes) > 0
    if using_threads:
        lookForWordsUsingThreds(words, indexes, file_text)
    else:
        lookForWordsIterative(words, file_text)

    global TOTAL
    print(f"{TOTAL} words had been found")


def lookForWordsIterative(words, file_text):
    for word in words:
        checkSpecificWordInFile(word, file_text)


def lookForWordsUsingThreds(words, indexes, file_text):
    threads = []
    for i in range(len(indexes)):
        temp = threading.Thread(target=lookWithinRange,
                                args=(words, indexes[0] + 1, i * indexes[0], i, file_text,))
        threads.append(temp)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def lookWithinRange(words, count, startIndex, thread_id, file_text, ):
    words_to_check = words[startIndex:startIndex + count]
    print(f"thread {thread_id} with starting index {startIndex} had started, he has {count} to check")

    for word in words_to_check:
        # print(f"startIndex) {startIndex}checking word - {word}")
        checkSpecificWordInFile(word, file_text)

    print(f"thread {thread_id}  had finished")


def checkSpecificWordInFile(word_user: str, file_text: str) -> bool:
    if word_user in file_text:
        updateTotalBy1()
        return True
    return False


def printSummery(start: float, end: float, using_threads: bool):
    print("using threads %s" % str(using_threads))
    print("done in %s seconds " % str(end - start))


def updateTotalBy1():
    global TOTAL
    TOTAL += 1


if __name__ == '__main__':
    main()
