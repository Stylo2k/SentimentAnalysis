## Description

Here you can find all the data sets that we have generated throughout our research. Personal identifiable information such as author and username tags have been removed or replaced in all local versions of our CSVs and JSONs. The original authors can still be identified, but not directly from our data set.

## Contents

- [Commits Analysis.csv](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Commits%20Analysis.csv) --> Final version of our Google Spreadsheets page that contains the labeled (cost taxonomy + sentiment analysis) commits.
- [Issue Analysis.csv](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Issue%20Analysis.csv) --> Final version of our Google Spreadsheets page that contains the labeled (cost taxonomy + sentiment analysis) issues.
- [Taxonomy and labels.xlsx](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Taxonomy%20and%20labels.xlsx) --> Microsoft Excel file containing our taxonomy and labels.
- [Commit mining/](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/tree/main/datasets/Commit%20Mining)
  - [terraform_keyworded.json](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Commit%20Mining/terraform_keyworded.json) --> JSON file containing all repositories that contain the keywords used for filtering
  - [terraform_tf_keywords.json](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Commit%20Mining/terraform_tf_keywords.json) --> JSON file containing all repositories that contain the keywords used for filtering, and had modifications on a ```.tf``` or ```.tf.json``` file.
- [Issue mining](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/tree/main/datasets/Issue%20Mining)
  - [terraform_issues.json](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Issue%20Mining/terraform_issues.json) --> JSON data for all issues and pull requests that contain the cost keywords used for filtering.
- [Repository mining](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/tree/main/datasets/Repository%20Mining)
  - [hclURLs.txt](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Repository%20Mining/hclURLs.txt) --> Contains the links to the repositories that contain ```hcl``` files.
  - [terraform_repos.txt](https://github.com/Max593/Mining-and-Analysis-of-Cost-related-Decisions-in-Cloud-Infrastructures/blob/main/datasets/Repository%20Mining/terraform_repos.txt) --> Contains the links to the repositories that contain ```hcl```, ```.tf```, and ```.tf.json``` files.
