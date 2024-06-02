#include <cctype>
#include <functional>
#include <iostream>
#include <istream>
#include <iterator>
#include <locale>
#include <map>
#include <ostream>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>
#include <vector>

std::multimap<int, std::string, std::greater<int> > word_count(std::basic_istream<char> &text) {
  std::unordered_map<std::string, int> word_counts;

  std::string word;
  char c;
  while (text.get(c)) {
    if (std::isalnum(c, std::locale::classic())) {
      word += std::tolower(c);
    } else if (word.empty()) {
      continue;
    } else {
      word_counts[word] += 1;
      word.clear();
    }
  }

  std::multimap<int, std::string, std::greater<int> > counted_words;
  for (std::pair<std::string, int> word_count: word_counts) {
    counted_words.insert(std::pair<int, std::string>(word_count.second, word_count.first));
  }

  return counted_words;
}

int main() {
  auto counted_words = word_count(std::cin);

  for (std::pair<int, std::string>counted_word: counted_words) {
    if (counted_word.second.length() < 7) {
    std::cout << counted_word.second << ":\t\t" << counted_word.first << std::endl;
      } else {
    std::cout << counted_word.second << ":\t" << counted_word.first << std::endl;
    }
  }
}