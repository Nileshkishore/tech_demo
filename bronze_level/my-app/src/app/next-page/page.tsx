import React from 'react';

// Define TypeScript interface for stock data
interface StockData {
  Symbol: string;
  Company_Name: string;
  Current: number;
  Current_Date: string;
  Currency: string;
  Today_Open: number;
  Today_Change: number;
  "1_Week_Change": number;
  "1_Month_Change": number;
  "1_Year_Change": number;
  "1_Week_Back_Date": string;
  "1_Month_Back_Date": string;
  "1_Year_Back_Date": string;
  Today_High: number;
  Today_Low: number;
  Weekly_Low: number;
  Weekly_High: number;
  Monthly_Low: number;
  Monthly_High: number;
  Yearly_Low: number;
  Yearly_High: number;
}

async function fetchStockData(): Promise<StockData[]> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/run-sqlonly3/?t=${new Date().getTime()}`);
  if (!response.ok) {
    throw new Error('Failed to fetch stock data');
  }
  const data = await response.json();
  return data;
}

function getChangeColor(value: number) {
  return value >= 0 ? 'text-green-500' : 'text-red-500';
}

export default async function Home() {
  let stockData: StockData[] = [];
  try {
    stockData = await fetchStockData();
  } catch (error) {
    console.error('Error fetching stock data:', error);
    // Handle the error gracefully
  }

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-4">Stock Data</h2>
      <div className="overflow-x-auto">
        <table className="w-full min-w-max border-collapse">
          <thead>
            <tr className="bg-gray-200">
              <th className="border border-gray-300 p-2">Symbol</th>
              <th className="border border-gray-300 p-2">Company Name</th>
              <th className="border border-gray-300 p-2">Current</th>
              <th className="border border-gray-300 p-2">Currency</th>
              <th className="border border-gray-300 p-2">Current Date</th>
              <th className="border border-gray-300 p-2">Today Open</th>
              <th className="border border-gray-300 p-2">Today Change</th>
              <th className="border border-gray-300 p-2">1 Week Change</th>
              <th className="border border-gray-300 p-2">1 Month Change</th>
              <th className="border border-gray-300 p-2">1 Year Change</th>
              <th className="border border-gray-300 p-2">1 Week Back Date</th>
              <th className="border border-gray-300 p-2">1 Month Back Date</th>
              <th className="border border-gray-300 p-2">1 Year Back Date</th>
              <th className="border border-gray-300 p-2">Today High</th>
              <th className="border border-gray-300 p-2">Today Low</th>
              <th className="border border-gray-300 p-2">Weekly High</th>
              <th className="border border-gray-300 p-2">Weekly Low</th>
              <th className="border border-gray-300 p-2">Monthly High</th>
              <th className="border border-gray-300 p-2">Monthly Low</th>
              <th className="border border-gray-300 p-2">Yearly High</th>
              <th className="border border-gray-300 p-2">Yearly Low</th>
            </tr>
          </thead>
          <tbody>
            {stockData.map((item, index) => {
              const todayChangeColor = getChangeColor(item.Today_Change);
              const oneWeekChangeColor = getChangeColor(item["1_Week_Change"]);
              const oneMonthChangeColor = getChangeColor(item["1_Month_Change"]);
              const oneYearChangeColor = getChangeColor(item["1_Year_Change"]);

              return (
                <tr key={index}>
                  <td className="border border-gray-300 p-2">{item.Symbol}</td>
                  <td className="border border-gray-300 p-2">{item.Company_Name}</td>
                  <td className="border border-gray-300 p-2">{item.Current.toFixed(2)}</td>
                  <td className="border border-gray-300 p-2">{item.Currency}</td>
                  <td className="border border-gray-300 p-2">{item.Current_Date}</td>
                  <td className="border border-gray-300 p-2">{item.Today_Open.toFixed(2)}</td>
                  <td className={`border border-gray-300 p-2 ${todayChangeColor} font-bold`}>
                    {item.Today_Change.toFixed(2)}%
                  </td>
                  <td className={`border border-gray-300 p-2 ${oneWeekChangeColor} font-bold`}>
                    {item["1_Week_Change"].toFixed(2)}%
                  </td>
                  <td className={`border border-gray-300 p-2 ${oneMonthChangeColor} font-bold`}>
                    {item["1_Month_Change"].toFixed(2)}%
                  </td>
                  <td className={`border border-gray-300 p-2 ${oneYearChangeColor} font-bold`}>
                    {item["1_Year_Change"].toFixed(2)}%
                  </td>
                  <td className="border border-gray-300 p-2 whitespace-nowrap">{item["1_Week_Back_Date"]}</td>
                  <td className="border border-gray-300 p-2 whitespace-nowrap">{item["1_Month_Back_Date"]}</td>
                  <td className="border border-gray-300 p-2 whitespace-nowrap">{item["1_Year_Back_Date"]}</td>
                  <td className="border border-gray-300 p-2">{item.Today_High}</td>
                  <td className="border border-gray-300 p-2">{item.Today_Low}</td>
                  <td className="border border-gray-300 p-2">{item.Weekly_High}</td>
                  <td className="border border-gray-300 p-2">{item.Weekly_Low}</td>
                  <td className="border border-gray-300 p-2">{item.Monthly_High}</td>
                  <td className="border border-gray-300 p-2">{item.Monthly_Low}</td>
                  <td className="border border-gray-300 p-2">{item.Yearly_High}</td>
                  <td className="border border-gray-300 p-2">{item.Yearly_Low}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
