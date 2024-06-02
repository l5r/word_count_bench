#include <bits/chrono.h>
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
#include <chrono>

std::multimap<int, std::string, std::greater<int> > word_count(std::basic_istream<char> &text) {
  using namespace std::chrono;

  std::unordered_map<std::string, int> word_counts;

  auto read_start_time_mono = steady_clock::now();
  auto read_start_time_wall = system_clock::now();

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

  auto read_duration_mono = duration_cast<milliseconds>(steady_clock::now() - read_start_time_mono);
  auto read_duration_wall = duration_cast<milliseconds>(system_clock::now() - read_start_time_wall);

  std::cerr << "read time (mono): " << read_duration_mono.count() << "ms" << std::endl;
  std::cerr << "read time (wall): " << read_duration_wall.count() << "ms" << std::endl;

  auto sort_start_time_mono = steady_clock::now();
  auto sort_start_time_wall = system_clock::now();

  std::multimap<int, std::string, std::greater<int> > counted_words;
  for (std::pair<std::string, int> word_count: word_counts) {
    counted_words.insert(std::pair<int, std::string>(word_count.second, word_count.first));
  }

  auto sort_duration_mono = duration_cast<milliseconds>(steady_clock::now() - sort_start_time_mono);
  auto sort_duration_wall = duration_cast<milliseconds>(system_clock::now() - sort_start_time_wall);

  std::cerr << "sort time (mono): " << sort_duration_mono.count() << "ms" << std::endl;
  std::cerr << "sort time (wall): " << sort_duration_wall.count() << "ms" << std::endl;

  return counted_words;
}

int main() {
  auto counted_words = word_count(std::cin);

  for (std::pair<int, std::string>counted_word: counted_words) {
    std::cout << counted_word.first << "\t" << counted_word.second << std::endl;
  }
}
