# Contributing to the Internship List
Thank you for your interest in contributing to the Pitt CSC and Simplify internship list!

Below, you'll find the guidelines for our repository. If you have any questions, please create a [miscellaneous issue](https://github.com/SimplifyJobs/Summer2026-Internships/issues/new/choose).

## Finding an Internship to Add
We ask that the internships that you add meet some requirements. Specifically, your internship must
- be in one of the following categories:
    - **Software Engineering** - Software development, computer engineering, full-stack, frontend, backend, mobile development
    - **Product Management** - Product manager, associate product manager (APM), product analyst roles
    - **Data Science, AI & Machine Learning** - Data science, machine learning, AI research, data engineering, analytics
    - **Quantitative Finance** - Quantitative trading, quantitative research, fintech engineering
    - **Hardware Engineering** - Hardware design, embedded systems, firmware, FPGA, circuit design
    - **Other** - Any other tech-related internships that don't fit the above categories
- be located in the United States, Canada, or remote.
- not already exist in the internship list.
- belong to a company using a formal ATS such as Workday, Greenhouse, Ashby, etc.
    - any company using non-ATS platforms such as forms or surveys must be verified/approved on Simplify.

## Adding an Internship
Cool! You're ready to add an internship to the list. Follow these steps:

1) First create a new issue [here](https://github.com/SimplifyJobs/Summer2026-Internships/issues/new/choose).
2) Select the **New Internship** issue template.
3) Fill in the information about your internship into the form, including:
   - **Category**: Choose the appropriate category from the dropdown (Software Engineering, Product Management, etc.)
   - **Advanced Degree Requirements**: Check this box if the internship specifically requires or prefers Master's, MBA, or PhD degrees
   - All other required fields (company, title, location, etc.)
4) Hit submit.
> Please make a new submission for each unique position, **even if they are for the same company**.
5) That's it! Once a member of our team has reviewed your submission, it will be automatically added to the correct `README` with proper categorization and degree indicators

## Editing an Internship
To edit an internship (changing name, setting as inactive, removing, etc.), follow these steps:
1) First copy the url of the internship you would like to edit.
> This can be found by right-clicking on the `APPLY` button and selecting **copy link address**
2) Create a new issue [here](https://github.com/SimplifyJobs/Summer2026-Internships/issues/new/choose).
3) Select the **Edit Internship** issue template.
4) Fill in the url to the **link** input.
> This is how we ensure your edit affects the correct internship
5) Leave every other input blank except for whichever fields you would like to update or change about the internship, including:
   - **Category**: Change the internship category if needed
   - **Advanced Degree Requirements**: Check or uncheck if the degree requirements have changed
   - Any other fields you want to modify
6) If it is not obvious why you are making these edits, please specify why in the reason box at the bottom of the form.
7) Hit submit. A member of our team will review your revision and approve it shortly.

## Automatic README.md Updates
A script will automatically add new contributions as well as new internships found by [Simplify](https://simplify.jobs) to the appropriate README. Internships will be:

- **Categorized** into the appropriate section (Software Engineering, Product Management, Data Science, etc.)
- **Marked with special indicators**:
  - 🔥 for FAANG+ companies (Google, Meta, Apple, Amazon, Microsoft, etc.)
  - 🎓 for roles requiring advanced degrees (Master's/MBA/PhD)
  - 🛂 for roles that don't offer sponsorship
  - 🇺🇸 for roles requiring U.S. citizenship

The row will look something like this:
```md
| Company | Role | Location | Application | Age |
| --- | --- | --- | :---: | :---: |
| 🔥 **[Google](https://google.com)** | Software Engineering Internship 🎓 | San Francisco, CA | <a href="..."><img src="..." alt="Apply"></a> | 2d |
```

When rendered, it will look like:
| Company | Role | Location | Application | Age |
| --- | --- | --- | :---: | :---: |
| 🔥 **[Google](https://google.com)** | Software Engineering Internship 🎓 | San Francisco, CA | <a href="..."><img src="..." alt="Apply"></a> | 2d |


