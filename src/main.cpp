#include <fstream>
#include <iostream>
#include <string>
#include <time.h>

int main() {

  std::string dstr, val1="0", val2="0";

  // date
  time_t timer = time(NULL);
  struct tm *date = localtime(&timer), input;
  std::cout << "Input date (default: ";
  std::cout << date->tm_year+1900 << "/"
	    << date->tm_mon+1 << "/"
	    << date->tm_mday;
  std::cout << "): ";
  std::getline(std::cin, dstr);
  if(dstr != "") {
    strptime(dstr.c_str(), "%Y/%m/%d", &input);
    input.tm_hour = 12;
    timer = std::mktime(&input);
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
  // (9 hours shift to use in the end of day)
  int serial = (int)((timer - 60 * 60 * 9) / (60 * 60 * 24));

  // output to file
  std::ofstream ofs("atm.dat", std::ios::app);
  ofs << serial << "\t"
      << val1 << "\t"
      << val2 << std::endl;
    
  return 0;
    
}
