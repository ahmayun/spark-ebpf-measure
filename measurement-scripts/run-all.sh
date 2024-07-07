echo "=========================== Q1 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q1 5 store_returns date_dim store customer
echo "=========================== Q3 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q3 5 store_sales date_dim item
echo "=========================== Q6 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q6 5 customer_address customer store_sales date_dim item
echo "=========================== Q7 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q7 5 customer_demographics promotion store_sales date_dim item
echo "=========================== Q12 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q12 5 web_sales date_dim item
echo "=========================== Q15 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q15 5 catalog_sales customer customer_address date_dim
echo "=========================== Q19 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q19 5 date_dim store_sales item customer customer_address store
echo "=========================== Q20 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh Q20 5 catalog_sales date_dim item
