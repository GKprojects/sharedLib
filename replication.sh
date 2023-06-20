#!/bin/bash

# Define the paths to the source and destination files
source_file="jobs/tools/restartDeploymentKF4/Jenkinsfile"
destination_file="jobs/tools/restartDeploymentKF3/Jenkinsfile"

# Define the lines in the destination file that should not be updated
preserve_line=""

# Read the content of the source and destination files
source_content=$(cat "$source_file")
destination_content=$(cat "$destination_file")

# Extract the value of the preserved line from the destination file
preserve_value=$(grep "$preserve_line" "$destination_file" | cut -d'=' -f2)

# Check if the source file has new changes
if [[ "$source_content" != "$destination_content" ]]; then
  # Generate the updated content with the preserved line
  if [[ "$preserve_line" ]]; then
    updated_content=$(echo "$source_content" | sed "s|$preserve_line.*|$preserve_line $preserve_value|")
  else
    updated_content=$(echo "$source_content")
  fi

  # Overwrite the destination file with the updated content
  echo "$updated_content" > "$destination_file"
fi
