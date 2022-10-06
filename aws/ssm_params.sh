aws --region eu-west-1 --profile AWS_PROFILE ssm describe-parameters --filters Key=Type,Values=String Key=Name,Values="/path/to/param" --output yaml | grep Name | awk '{print $2}' | while read f; do
echo $f;aws --region eu-west-1 --profile AWS_PROFILE ssm get-parameter --name $f --output yaml | grep Value;
done
