#include <time.h>

#include <boost/algorithm/string.hpp>
#include <fstream>
#include <iostream>
#include <string>

int main()
{

  std::string dstr, val1 = "0", val2 = "0";

  // date
  time_t timer = time(NULL) - 60 * 60 * 3;
  struct tm *date = localtime(&timer), input;
  std::cout << "Input date from today (n <= 0) (default: ";
  std::cout << date->tm_year + 1900 << "/" << date->tm_mon + 1 << "/"
            << date->tm_mday;
  std::cout << "): ";
  std::getline(std::cin, dstr);
  if (dstr != "")
  {
    // std::mktime not working properly on macOS arm 2020/12/11
    // strptime(dstr.c_str(), "%Y/%m/%d", &input);
    // input.tm_hour = 12;
    // timer = std::mktime(&input);
    int n = stoi(dstr);
    timer += n * 60 * 60 * 24;

    // std::cout << input.tm_year+1900 << "/"
    // 	      << input.tm_mon+1 << "/"
    // 	      << input.tm_mday;
  }

  // workload
  std::cout << "How hard did you work? (rate by [0-3]): ";
  std::getline(std::cin, val1);

  // mood
  std::cout << "How was your mood? (rate by [0-2]): ";
  std::getline(std::cin, val2);

  // convert to serial in unit of days
  // (Use Berkeley Time)
  int serial = (int)((timer - 60 * 60 * 8) / (60 * 60 * 24));

  // output to file
  std::ofstream ofs("atm.dat", std::ios::app);
  ofs << serial << "\t" << val1 << "\t" << val2 << std::endl;

  return 0;
}
