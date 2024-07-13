TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
export GLOBAL_LOG_FILE="/home/ahmad/Desktop/bpf-playground/learning-ebpf/chapter3/spark-ebpf-measure/results/global_logs/gl_run_$TIMESTAMP"
echo "=========================== Q1 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q1 5 store_returns_l1 date_dim_l1 store_l1 customer_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q1 5 store_returns_l2 date_dim_l2 store_l2 customer_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q1 5 store_returns_l3 date_dim_l3 store_l3 customer_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q1 5 store_returns_l4 date_dim_l4 store_l4 customer_l4

echo "=========================== Q3 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q3 5 store_sales_l1 date_dim_l1 item_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q3 5 store_sales_l2 date_dim_l2 item_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q3 5 store_sales_l3 date_dim_l3 item_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q3 5 store_sales_l4 date_dim_l4 item_l4

echo "=========================== Q6 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q6 5 customer_address_l1 customer_l1 store_sales_l1 date_dim_l1 item_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q6 5 customer_address_l2 customer_l2 store_sales_l2 date_dim_l2 item_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q6 5 customer_address_l3 customer_l3 store_sales_l3 date_dim_l3 item_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q6 5 customer_address_l4 customer_l4 store_sales_l4 date_dim_l4 item_l4

echo "=========================== Q7 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q7 5 customer_demographics_l1 promotion_l1 store_sales_l1 date_dim_l1 item_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q7 5 customer_demographics_l2 promotion_l2 store_sales_l2 date_dim_l2 item_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q7 5 customer_demographics_l3 promotion_l3 store_sales_l3 date_dim_l3 item_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q7 5 customer_demographics_l4 promotion_l4 store_sales_l4 date_dim_l4 item_l4

echo "=========================== Q12 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q12 5 web_sales_l1 date_dim_l1 item_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q12 5 web_sales_l2 date_dim_l2 item_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q12 5 web_sales_l3 date_dim_l3 item_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q12 5 web_sales_l4 date_dim_l4 item_l4

echo "=========================== Q15 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q15 5 catalog_sales_l1 customer_l1 customer_address_l1 date_dim_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q15 5 catalog_sales_l2 customer_l2 customer_address_l2 date_dim_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q15 5 catalog_sales_l3 customer_l3 customer_address_l3 date_dim_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q15 5 catalog_sales_l4 customer_l4 customer_address_l4 date_dim_l4

echo "=========================== Q19 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q19 5 date_dim_l1 store_sales_l1 item_l1 customer_l1 customer_address_l1 store_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q19 5 date_dim_l2 store_sales_l2 item_l2 customer_l2 customer_address_l2 store_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q19 5 date_dim_l3 store_sales_l3 item_l3 customer_l3 customer_address_l3 store_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q19 5 date_dim_l4 store_sales_l4 item_l4 customer_l4 customer_address_l4 store_l4

echo "=========================== Q20 ============================"
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l1 Q20 5 catalog_sales_l1 date_dim_l1 item_l1
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l2 Q20 5 catalog_sales_l2 date_dim_l2 item_l2
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l3 Q20 5 catalog_sales_l3 date_dim_l3 item_l3
./measurement-scripts/convenience-wrapper-kernel-stack-time.sh l4 Q20 5 catalog_sales_l4 date_dim_l4 item_l4
