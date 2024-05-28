# Set the working directory
setwd("~/Documents/Github/Welfare2")

library(tidyverse)
library(purrr)
library(jsonlite)
library(extrafont)

# Import the CM Roman font
font_import(pattern = "cmunrm.ttf")
# Load the fonts
loadfonts()

# Specify the directory and subfolders
data_folder <- file.path(getwd(), "Data")
folder_name <- "2023-08-main_sample"

# Construct the path to the folder
folder_path <- file.path(data_folder, folder_name)

# Get a list of all files in the specified folder
files <- list.files(folder_path, full.names = TRUE)

# Filter the file names to find the one that starts with 'all_apps_wide'
csv_file <- files[grep("^all_apps_wide", basename(files))]

# Check if a CSV file was found
if (length(csv_file) == 0) {
  print("No CSV file starting with 'all_apps_wide' found.")
} else {
  # Read the CSV file
  data_raw <- read.csv(csv_file) 
}

# List 1 Shannon: opposite; List 2 Isha: original; List 3 Haley: opposite;  
# List of file names to reverse rows for
reverse_list <- c("List 1", "List 3")

# Filter the file names to find the one that starts with 'Welfare'
csv_files <- files[grep("^Welfare.*\\.csv$", basename(files))]

# Extract the names from the paths
file_names <- substring(csv_files, 
                        first = regexpr("Welfare Project_ Classification of Answers - ", csv_files) + nchar("Welfare Project_ Classification of Answers - "),
                        last = regexpr("\\.csv$", csv_files) - 1)

# Extract the first 5 characters: List X
file_names <- substr(file_names, 1, 6)

# Initialize an empty list to store data frames
data_frames <- list()

# Loop through each file in filenames
for (file in csv_files) {
  # Extract the file name
  file_name <- substr(file, regexpr("Welfare Project_ Classification of Answers - ", file) + nchar("Welfare Project_ Classification of Answers - "), regexpr("\\.csv$", file) - 1)
  file_name <- substr(file_name, 1, 6)
  # Read the CSV file
  data_temp <- read.csv(file, skip=1)
  
  names(data_temp) <- gsub("\\.", "", names(data_temp))
  
  # List of column names to convert to lowercase and remove leading/trailing spaces
  columns_to_clean <- c("Misunderstanding", "ChatGPT", "Inconsistent", "Understandsdifferencebetweencases")
  
  # Convert values in specified columns to lowercase and remove leading/trailing spaces
  data_temp[columns_to_clean] <- lapply(data_temp[columns_to_clean], function(x) trimws(tolower(x)))
  
  # Rename columns
  colnames(data_temp) <- paste0(names(data_temp), "_", file_name)
  
  # Check if file_name is in the reverse_list
  if (file_name %in% reverse_list) {
    # Reverse the rows
    data_temp <- data_temp[nrow(data_temp):1, ]
  }
  
  # Append the data frame to the list
  data_frames[[length(data_frames) + 1]] <- data_temp
}

# Concatenate the data frames
result<- do.call(cbind, data_frames)

# Define a function to find the mode of a vector
Mode <- function(...) {
  ux <- unique(c(...))
  ux[which.max(tabulate(match(c(...), ux)))]
}

# Apply the Mode function to each row of specific columns in your data frame and store the results in new columns
result <- result %>%
  filter(`MPLWhy_List 2` != "Whatevs") %>%
  mutate(`MPLWhy_List 2` = trimws(`MPLWhy_List 2`)) %>%
  mutate(modal_misunderstanding = apply(select(., starts_with("Misunderstanding")), 1, Mode),
         modal_inconsistent = apply(select(., starts_with("Inconsistent")), 1, Mode), 
         modal_ChatGPT = apply(select(., starts_with("ChatGPT")), 1, Mode), 
         modal_understands = apply(select(., starts_with("Understandsdifferencebetweencases")), 1, Mode)) %>%

  # Add a new column based on the extended conditions
  mutate(all_conditions_met = (modal_misunderstanding == "no" & 
                                 modal_inconsistent == "no" & 
                                 modal_ChatGPT == "no"))

# Restrict to participants who finished
data <- data_raw %>%
  filter(session.code == "hyxtp0i1") %>%
  mutate(finished = participant._current_page_name %in% c("Finished", "End")) %>%
  filter(finished == TRUE) %>%
  mutate(welfare.2.player.MPLWhy = trimws(welfare.2.player.MPLWhy))

# Combine RAs classifications with Prolific data
data <- cbind(result, data)

# Rename columns for unincentivized questions
data <- data %>%
  rename(experience = welfare.2.player.experience,
         arkansas = welfare.2.player.arkansas,
         warhol = welfare.2.player.warhol)

# experience: 1-> Yes (MS); 0-> No (ES)
# arkansas: 1-> Better off (ES); 0-> Worse off (MS)
# warhol: 1-> Yes (ES); 0-> No (MS)

# Standardize data in unincentivized columns
data <- data %>%
  mutate(experience = ifelse(experience, "MS", "ES"),
         arkansas = ifelse(arkansas, "ES", "MS"),
         warhol = ifelse(warhol, "ES", "MS"))

# Create a new column describing answers to all three unincentivized questions
data <- data %>%
  mutate(unincentivized_types = case_when(
    warhol == "MS" & experience == "MS" & arkansas == "MS" ~ "MS",
    warhol == "ES" & experience == "ES" & arkansas == "ES" ~ "ES",
    TRUE ~ "mixed"
  ))

# defined ES_wtp data based on last recorded measures: pick welfare.2.player if exists; otherwise pick welfare.1.player
data <- data %>%
  mutate(ES_wtp1 = if_else(!is.na(welfare.2.player.ES_wtp), welfare.2.player.ES_wtp, welfare.1.player.ES_wtp)) %>%
  mutate(Trad_wtp1 = if_else(!is.na(welfare.2.player.Trad_wtp), welfare.2.player.Trad_wtp, welfare.1.player.Trad_wtp)) %>%
  
  mutate(ES_wtp2 = if_else(!is.na(welfare.2.player.ES_wtp2), welfare.2.player.ES_wtp2, welfare.1.player.ES_wtp2)) %>%
  mutate(Trad_wtp2 = if_else(!is.na(welfare.2.player.Trad_wtp2), welfare.2.player.Trad_wtp2, welfare.1.player.Trad_wtp2)) %>%
  
  mutate(ES_wtp3 = if_else(welfare.2.player.ES_wtp3!="", welfare.2.player.ES_wtp3, welfare.1.player.ES_wtp3)) %>%
  mutate(Trad_wtp3 = if_else(welfare.2.player.Trad_wtp3!="", welfare.2.player.Trad_wtp3, welfare.1.player.Trad_wtp3)) 


#### Create WTP column for Learn and NotLearns cases
# ES_wtp1: 1=Original, 2=Fake, 3=Indifferent
# Trad_wtp1: 1=Original, 2=Fake, 3=Indifferent

# ES_wtp2: 1=Original, 2=Fake
# Trad_wtp2: 1=Original, 2=Fake
# Note: the options may have money attached to them depending on ES_wtp, Trad_wtp

# ES_wtp3 and Trad_wtp3
# WTP_values: [2, 3, 5, 7, 10, 15, 25, 45, 70, 100, 140, 200]
# [1, 3, 6] Left: Original + $0; Right: Fake + $X dollars. 

WTP_values <- list(1, 2, 3, 5, 7, 10, 15, 25, 45, 70, 100, 140, 200, 200)
# answer looks like: {...,"cutoff":"right:i"}; means: I prefer right:i and all below
# --> right:0 --> 1+2 / 2: list1+list2/2 ... list:i+1 + list:i+2 / 2 
# --> right:1 --> 2+3 / 2
# ... right:11 --> 140+200 /2 

# or {...,cutoff":"left:i"}, where i is the i-1-th row ; means: I prefer left i and all above
# --> left:0 --> 2+3 /2 : list2+list3/2 ... list:i+2 + list:i+3 / 2 

# [2, 4, 5] Left: Fake + $X; Right: Original + $0. 
# answer looks like: {...,"cutoff":"right:i"}; means: I prefer right:i and all above
# or {...,cutoff":"left:i"}, where i is the i-1-th row ; means: I prefer left i and all below
# --> right:0 --> 2+3 / 2: list2+list3/2 ... list:i+2 + list:i+3 / 2 
# --> left:0 --> 1+2 / 2: list1+list2/2 ... list:i+1 + list:i+2 / 2 

# Extract the cutoff from wtp3
data <- data %>%
  mutate(ES_cutoff = lapply(ES_wtp3, function(x) {
    tryCatch({
      parsed_json <- fromJSON(x)
      unlist(parsed_json$cutoff)
    }, error = function(e) {
      "NOT A VALID JSON"
    })
  })) %>%
  mutate(Trad_cutoff = lapply(Trad_wtp3, function(x) {
    tryCatch({
      parsed_json <- fromJSON(x)
      unlist(parsed_json$cutoff)
  
    }, error = function(e) {
      "NOT A VALID JSON"
    })
  }))
      
data <- data %>%
  mutate(Trad_cutoff = sapply(Trad_cutoff, function(x) {
    if (length(x) > 0) {
      x[[1]]  # Extract the first element of each list
    } else {
      NA  # If the list is empty or NULL, return NA
    }
  }))

data <- data %>%
  mutate(ES_cutoff = sapply(ES_cutoff, function(x) {
    if (length(x) > 0) {
      x[[1]]  # Extract the first element of each list
    } else {
      NA  # If the list is empty or NULL, return NA
    }
  }))

# Simple cases for WTP
data <- data %>%
  mutate(ES_wtp = if_else(ES_wtp1 == 3, 0, NA_real_)) %>%
  mutate(Trad_wtp = if_else(Trad_wtp1 == 3, 0, NA_real_)) %>%
  # 
  mutate(ES_wtp = if_else((ES_wtp1 == 1 & ES_wtp2 == 2) | (ES_wtp1 == 2 & ES_wtp2 == 1), 0, ES_wtp)) %>%
  mutate(Trad_wtp = if_else((Trad_wtp1 == 1 & Trad_wtp2 == 2) | (Trad_wtp1 == 2 & Trad_wtp2 == 1), 0, Trad_wtp)) %>%

  
  mutate(ES_wtp = if_else(ES_wtp1 == 2 & ES_wtp2 == 2, -1, ES_wtp)) %>%
  mutate(Trad_wtp = if_else(Trad_wtp1 == 2 & Trad_wtp2 == 2, -1, Trad_wtp)) 
  
# Extract wtp from wtp3
extract_value <- function(x,choices) {
  if (grepl("right:", x)) {
    i <- as.numeric(gsub("right:", "", x))
    if (choices %in% c(1, 3, 6)) {
      return((as.numeric(WTP_values[i+1]) + as.numeric(WTP_values[i + 2])) / 2) 
    } else {
      return((as.numeric(WTP_values[i+2]) + as.numeric(WTP_values[i + 3])) / 2)
    }
  } else if (grepl("left:", x)) {
   
    i <- as.numeric(gsub("left:", "", x))
    if (choices %in% c(1, 3, 6)) {
      return((as.numeric(WTP_values[i + 2]) + as.numeric(WTP_values[i + 3])) / 2)
    } else {
      return((as.numeric(WTP_values[i+1]) + as.numeric(WTP_values[i + 2])) / 2) 
    }
  } else {
    return('No WTP3 recorded')
  } 
}

# Apply the function to the original column using mutate
data <- data %>%
  rowwise() %>%
  mutate(ES_wtp = ifelse(ES_cutoff == "NOT A VALID JSON",ES_wtp, extract_value(ES_cutoff,participant.choices_orders))) %>%
  mutate(Trad_wtp =  ifelse(Trad_cutoff == "NOT A VALID JSON",Trad_wtp, extract_value(Trad_cutoff,participant.choices_orders)))

# Create new column based on participant.treatment
data <- data %>%
  mutate(treatment = case_when(
    participant.treatment == "middle" ~ "Baseline",
    participant.treatment == "low" ~ "LowMS",
    participant.treatment == "high" ~ "HighMS",
    TRUE ~ NA_character_  # Handle other cases
  ))

data <- data %>% 
  mutate(ratio = ES_wtp / Trad_wtp) %>%
  mutate(ES_bin = ifelse(ratio == 1, 1, 0)) %>%
  mutate(MS_bin = ifelse(ratio == 0, 1, 0))
  

# Table 1
calculate_share_category <- function(data,xvar) {
  df_shares <- data %>%
    mutate(share_category = case_when(
      (Trad_wtp < 0) & (ES_wtp < 0) ~ "01Trad_WTP_less_than_0_and_ES_wtp_less_than_0",
      (Trad_wtp < 0) & (ES_wtp == 0) ~ "02Trad_WTP_less_than_0_and_ES_wtp_equal_to_0",
      (Trad_wtp < 0) & (ES_wtp > 0) ~ "03Trad_WTP_less_than_0_and_ES_wtp_greater_than_0",
      (Trad_wtp == 0) & (ES_wtp < 0) ~ "04Trad_WTP_equal_to_0_and_ES_wtp_less_than_0",
      (Trad_wtp == 0) & (ES_wtp == 0) ~ "05Trad_WTP_equal_to_0_and_ES_wtp_equal_to_0",
      (Trad_wtp == 0) & (ES_wtp > 0) ~ "06Trad_WTP_equal_to_0_and_ES_wtp_greater_than_0",
      (Trad_wtp > 0) & (ES_wtp < 0) ~ "07Trad_WTP_greater_than_0_and_ES_wtp_less_than_0",
      (Trad_wtp > 0) & (ES_wtp == 0) ~ "08Trad_WTP_greater_than_0_and_ES_wtp_equal_to_0",
      (Trad_wtp > 0) & (Trad_wtp > ES_wtp) & (ES_wtp > 0) ~ "09Trad_WTP_greater_than_0_and_ES_wtp_greater_than_0",
      (Trad_wtp > 0) & (Trad_wtp == ES_wtp) ~ "10Trad_WTP_greater_than_0_and_ES_wtp_equal_to_Trad_WTP",
      (Trad_wtp > 0) & (Trad_wtp < ES_wtp) ~ "11Trad_WTP_greater_than_0_and_ES_wtp_greater_than_Trad_WTP"
    )) %>%
    group_by({{xvar}}, share_category) %>%
    summarize(share = n()) %>%
    ungroup() %>%
    group_by({{xvar}}) %>%
    mutate(share = sprintf("%.2f", round(share * 100 / sum(share), 2))) 
  
  return(df_shares)
}

# Table 1
myshares <- calculate_share_category(data,treatment)
print(n = 200, myshares)

# Table 3
myshares <- calculate_share_category(data,warhol)
print(n = 200, myshares)

myshares <- calculate_share_category(data,experience)
print(n = 200, myshares)

myshares <- calculate_share_category(data,arkansas)
print(n = 200, myshares)

# Filter the dataset to select rows where the new column is either "MS" or "ES"
data_for_unincentivized_types <- data %>%
  filter(unincentivized_types %in% c("MS", "ES"))

myshares <- calculate_share_category(data_for_unincentivized_types,unincentivized_types)
print(n = 200, myshares)


data_quality <- data %>%
  filter(all_conditions_met == TRUE)

# Table 2
myshares <- calculate_share_category(data_quality,treatment)
print(n = 200, myshares)

# Table 4
myshares <- calculate_share_category(data_quality,warhol)
print(n = 200, myshares)

myshares <- calculate_share_category(data_quality,experience)
print(n = 200, myshares)

myshares <- calculate_share_category(data_quality,arkansas)
print(n = 200, myshares)

# Filter the dataset to select rows where the new column is either "MS" or "ES"
data_for_unincentivized_types <- data_quality %>%
  filter(unincentivized_types %in% c("MS", "ES"))

myshares <- calculate_share_category(data_for_unincentivized_types,unincentivized_types)
print(n = 200, myshares)



# Select columns of interest
columns_of_interest <- c("ES_wtp","ESWTP_List 1", "participant.choices_orders","Trad_cutoff")

# Print the first 5 rows of selected columns
print(n=100,data[1:100, columns_of_interest])


theme_set(theme_minimal(base_family = "CMU Serif"))
plot_cdf <- function(data, x_variable) {
  ggplot(data, aes(x = {{x_variable}}, color = treatment, linetype = treatment)) +
    stat_ecdf(geom = "step", linewidth = 1) +
    scale_x_continuous(breaks = c(0, 50, 100, 150, 200), labels = c(0, 50, 100, 150, 200)) +
    scale_y_continuous(breaks = seq(0, 1, 0.2), labels = sprintf("%.1f", seq(0, 1, 0.2)),
                       minor_breaks = seq(0, 1, 0.1)) +
    labs(x = "Values") + 
    theme(axis.title.y = element_blank(), 
          axis.text.x = element_text(size = 12),  # Set font size to 12pt for x-axis labels
          axis.text.y = element_text(size = 12),  # Set font size to 12pt for y-axis labels
          axis.ticks.x = element_line(color = "black", size = 0.5),  # Add small ticks at x-axis labels
          axis.ticks.y = element_line(color = "black", size = 0.5),  # Add small ticks at y-axis labels
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(), plot.title = element_blank(),
          panel.border = element_rect(color = "black", fill = NA, size = 1),
          legend.background = element_rect(color = "black", fill = NA, size = 1)) +
    scale_color_manual(values = c("Baseline" = "lightgrey", "LowMS" = "black", "HighMS" = "black"),
                       breaks = c("Baseline", "LowMS", "HighMS"),
                       labels = c("Baseline", "LowMS", "HighMS")) +
    scale_linetype_manual(values = c("Baseline" = "solid", "LowMS" = "longdash", "HighMS" = "solid"),
                          breaks = c("Baseline", "LowMS", "HighMS"),
                          labels = c("Baseline", "LowMS", "HighMS")) +
    guides(color = guide_legend()) +
    theme(legend.position = c(0.8, 0.35), legend.title = element_blank(), 
          legend.text = element_text(size = 12),  # Set font size to 12pt for legend
          legend.key.size = unit(1.5, "lines"),
          legend.key.height = unit(2, "lines"), 
          legend.key.width = unit(4, "lines"),
          axis.title.x = element_text(size=12))
}


# Example usage
p1 <- plot_cdf(data, ES_wtp)
ggsave(file.path("Output", folder_name, "Figure1a.png"), plot = p1, width = 5, height = 3, units = "in", bg='white')

p1 <- plot_cdf(data, Trad_wtp)
ggsave(file.path("Output", folder_name, "Figure1b.png"), plot = p1, width = 5, height = 3, units = "in", bg='white')


plot_cdf2 <- function(data, question) {
  ggplot(data, aes(x = ES_wtp / Trad_wtp, color = {{question}}, linetype = {{question}})) +
    stat_ecdf(geom = "step", linewidth = 1) +
    scale_x_continuous(breaks = seq(0, 1, 0.2), labels = sprintf("%.1f", seq(0, 1, 0.2))) +
    scale_y_continuous(breaks = seq(0, 1, 0.2), labels = sprintf("%.1f", seq(0, 1, 0.2)),
                       minor_breaks = seq(0, 1, 0.1)) +
    labs(x = "Ratios") + 
    coord_cartesian(xlim = c(0, 1)) +
    theme(axis.title.y = element_blank(),
          axis.title.x = element_text(size=12),
          axis.text.x = element_text(size = 12),  # Set font size to 12pt for x-axis labels
          axis.text.y = element_text(size = 12),  # Set font size to 12pt for y-axis labels
          axis.ticks.x = element_line(color = "black", size = 0.5),  # Add small ticks at x-axis labels
          axis.ticks.y = element_line(color = "black", size = 0.5),  # Add small ticks at y-axis labels
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(), plot.title = element_blank(),
          panel.border = element_rect(color = "black", fill = NA, size = 1),
          legend.background = element_rect(color = "black", fill = NA, size = 1),
          legend.position = c(0.2, 0.725), legend.title = element_blank(), 
          legend.text = element_text(size = 12),  # Set font size to 12pt for legend
          legend.key.size = unit(1.5, "lines"),
          legend.key.height = unit(2, "lines"), 
          legend.key.width = unit(4, "lines")) +  # Remove legend title
    scale_color_manual(values = c("MS" = "lightgray", "ES" = "black"),  # Set line colors
                       breaks = c("MS", "ES"),  # Set legend order
                       labels = c("MS", "ES")) +  # Set legend labels
    scale_linetype_manual(values = c("MS" = "solid", "ES" = "solid"),  # Set line types
                          breaks = c("MS", "ES"),  # Set legend order
                          labels = c("MS", "ES"))  # Set legend labels
}

filtered_data <- data %>%
  filter(Trad_wtp > 0)


p1 <- plot_cdf2(filtered_data, warhol)
ggsave(file.path("Output", folder_name, "Figure2warhol.png"), plot = p1, width = 5, height = 3, units = "in", bg='white')

p1 <- plot_cdf2(filtered_data, experience)
ggsave(file.path("Output", folder_name, "Figure2experience.png"), plot = p1, width = 5, height = 3, units = "in", bg='white')

p1 <- plot_cdf2(filtered_data, arkansas)
ggsave(file.path("Output", folder_name, "Figure2arkansas.png"), plot = p1, width = 5, height = 3, units = "in", bg='white')



data_for_unincentivized_types <- filtered_data %>%
  filter(unincentivized_types %in% c("MS", "ES"))


p1 <- plot_cdf2(data_for_unincentivized_types, unincentivized_types)
ggsave(file.path("Output", folder_name, "Figure2all.png"), plot = p1, width = 5, height = 3, units = "in", bg='white')

print(table(data_for_unincentivized_types$unincentivized_types))

ks_result <- ks.test(data$ES_wtp[data$treatment == 'HighMS'], data$ES_wtp[data$treatment == 'LowMS'])
print(ks_result)

ks_result <- ks.test(data$Trad_wtp[data$treatment == 'HighMS'], data$Trad_wtp[data$treatment == 'LowMS'])
print(ks_result)



ks_result <- ks.test(filtered_data$ratio[filtered_data$warhol == 'MS'], filtered_data$ratio[filtered_data$warhol == 'ES'])
print(ks_result)

ks_result <- ks.test(filtered_data$ratio[filtered_data$experience == 'MS'], filtered_data$ratio[filtered_data$experience == 'ES'])
print(ks_result)

ks_result <- ks.test(filtered_data$ratio[filtered_data$arkansas == 'MS'], filtered_data$ratio[filtered_data$arkansas == 'ES'])
print(ks_result)

ks_result <- ks.test(data_for_unincentivized_types$ratio[data_for_unincentivized_types$unincentivized_types == 'MS'], data_for_unincentivized_types$ratio[data_for_unincentivized_types$unincentivized_types == 'ES'])
print(ks_result)




calculate_share_summary <- function(data, group_column) {
  # Group the data by the specified column and calculate the shares
  share_summary <- data %>%
    group_by({{ group_column }}) %>%
    summarize(
      pureMS = sprintf("%.4f", mean(ratio == 0)),
      pureES = sprintf("%.4f", mean(ratio == 1))
    )
  
  # Print the summary
  print(share_summary)
}

# Numbers used in the manuscript:

# Call the function with your dataset and the column name "warhol"
calculate_share_summary(filtered_data, warhol)
calculate_share_summary(filtered_data, experience)
calculate_share_summary(filtered_data, arkansas)
calculate_share_summary(data_for_unincentivized_types, unincentivized_types)

t.test(filtered_data[filtered_data$experience=="MS",]$MS_bin,filtered_data[filtered_data$experience=="ES",]$MS_bin)
t.test(filtered_data[filtered_data$experience=="MS",]$ES_bin,filtered_data[filtered_data$experience=="ES",]$ES_bin)

t.test(filtered_data[filtered_data$arkansas=="MS",]$MS_bin,filtered_data[filtered_data$arkansas=="ES",]$MS_bin)
t.test(filtered_data[filtered_data$arkansas=="MS",]$ES_bin,filtered_data[filtered_data$arkansas=="ES",]$ES_bin)

t.test(filtered_data[filtered_data$warhol=="MS",]$MS_bin,filtered_data[filtered_data$warhol=="ES",]$MS_bin)
t.test(filtered_data[filtered_data$warhol=="MS",]$ES_bin,filtered_data[filtered_data$warhol=="ES",]$ES_bin)

t.test(data_for_unincentivized_types[data_for_unincentivized_types$unincentivized_types=="MS",]$MS_bin,data_for_unincentivized_types[data_for_unincentivized_types$unincentivized_types=="ES",]$MS_bin)
t.test(data_for_unincentivized_types[data_for_unincentivized_types$unincentivized_types=="MS",]$ES_bin,data_for_unincentivized_types[data_for_unincentivized_types$unincentivized_types=="ES",]$ES_bin)


# share of participants in baseline with positive Trad_wtp
share_baseline_pos_trad_wtp <- mean(data[data$treatment == 'Baseline',]$Trad_wtp>0)
print(share_baseline_pos_trad_wtp)

conditional_data <- data[data$treatment == 'Baseline' & data$Trad_wtp<=0,]
print(mean(conditional_data$ES_wtp==0))


conditional_data <- data[data$treatment == 'Baseline' & data$Trad_wtp>0,]

print(mean(conditional_data$ES_wtp==0))

print(mean(conditional_data$ES_wtp>0 & conditional_data$ES_wtp<conditional_data$Trad_wtp))

print(mean(conditional_data$ES_wtp==conditional_data$Trad_wtp))


conditional_data <- data[data$treatment == 'HighMS',]
print(mean(conditional_data$Trad_wtp>0))


conditional_data <- data[data$treatment == 'LowMS',]
print(mean(conditional_data$Trad_wtp>0))


freq_table <- table(data$experience)
# Calculate the share of each value
share_values <- prop.table(freq_table)
# Print the share of each value
print(share_values)

freq_table <- table(data$warhol)
# Calculate the share of each value
share_values <- prop.table(freq_table)
# Print the share of each value
print(share_values)

freq_table <- table(data$arkansas)
# Calculate the share of each value
share_values <- prop.table(freq_table)
# Print the share of each value
print(share_values)





