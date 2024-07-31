import React from 'react';
import { FaArrowUp, FaArrowDown } from 'react-icons/fa';

// Define TypeScript interface for stock data
interface StockData {
  Company_Name: string;
  Current: number;
  Currency: string;
  Today_Open: number;
  Today_High: number;
  Today_Low: number;
  Today_Change: number;
  "1_Week_Change": number;
  "1_Month_Change": number;
  "1_Year_Change": number;
  "Current_Date": string; // Current date
  "1_Week_Back_Date": string; // Date one week ago
  "1_Month_Back_Date": string; // Date one month ago
  "1_Year_Back_Date": string; // Date one year ago
}

// Fetch stock data from the API
const fetchStockData = async (): Promise<StockData[]> => {
  const response = await fetch(`http://127.0.0.1:8000/api/run-sqlonly3/?t=${new Date().getTime()}`);
  if (!response.ok) throw new Error('Failed to fetch stock data');
  return response.json();
};

// Get the top gainer or loser based on the period
const getExtreme = (stockData: StockData[], period: keyof StockData, isMax: boolean) => {
  return stockData.reduce((extreme, item) => {
    const value = item[period];
    if (isMax ? value > extreme.Value : value < extreme.Value) {
      return { Company_Name: item.Company_Name, Value: value };
    }
    return extreme;
  }, { Company_Name: '', Value: isMax ? -Infinity : Infinity });
};

export default async function Home() {
  let stockData: StockData[] = [];
  try {
    stockData = await fetchStockData();
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }

  const periods: (keyof StockData)[] = ['Today_Change', '1_Week_Change', '1_Month_Change', '1_Year_Change'];

  const topGainers = periods.reduce((acc, period) => ({
    ...acc,
    [period]: getExtreme(stockData, period, true)
  }), {} as Record<string, { Company_Name: string; Value: number }>);

  const topLosers = periods.reduce((acc, period) => ({
    ...acc,
    [period]: getExtreme(stockData, period, false)
  }), {} as Record<string, { Company_Name: string; Value: number }>);

  return (
    <div className="p-8">
      {/* Top Gainers and Losers */}
      <div className="mb-8 grid grid-cols-2 gap-4">
        {/* Top Gainers */}
        <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-lg shadow-lg flex flex-col items-center">
          <FaArrowUp className="text-4xl mb-4" />
          <h3 className="text-2xl font-bold mb-2">Top Gainers</h3>
          <div className="space-y-2 w-full">
            <div className="bg-white text-green-800 p-4 rounded-lg shadow-md">
              {periods.map(period => (
                <p key={period} className="font-semibold">
                  {period.replace('_', ' ')}: {topGainers[period].Company_Name} ({topGainers[period].Value.toFixed(2)}%)
                </p>
              ))}
            </div>
          </div>
        </div>

        {/* Top Losers */}
        <div className="bg-gradient-to-r from-red-500 to-red-600 text-white p-6 rounded-lg shadow-lg flex flex-col items-center">
          <FaArrowDown className="text-4xl mb-4" />
          <h3 className="text-2xl font-bold mb-2">Top Losers</h3>
          <div className="space-y-2 w-full">
            <div className="bg-white text-red-800 p-4 rounded-lg shadow-md">
              {periods.map(period => (
                <p key={period} className="font-semibold">
                  {period.replace('_', ' ')}: {topLosers[period].Company_Name} ({topLosers[period].Value.toFixed(2)}%)
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Last Recorded Data About Stocks */}
      <div className="mb-8">
        <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-bold mb-4">Last Recorded Data About Stocks</h3>
          <div className="overflow-x-auto">
            <table className="w-full min-w-max border-collapse bg-white text-blue-800 rounded-lg shadow-md">
              <thead className="bg-blue-700 text-white">
                <tr>
                  <th className="border border-blue-600 p-2">Company Name</th>
                  <th className="border border-blue-600 p-2">Current Price</th>
                  <th className="border border-blue-600 p-2">Today's High</th>
                  <th className="border border-blue-600 p-2">Today's Low</th>
                  <th className="border border-blue-600 p-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {stockData.map((item, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-blue-50' : 'bg-blue-100'}>
                    <td className="border border-blue-600 p-2">{item.Company_Name}</td>
                    <td className="border border-blue-600 p-2">{item.Current.toFixed(2)} {item.Currency}</td>
                    <td className="border border-blue-600 p-2">{item.Today_High.toFixed(2)} {item.Currency}</td>
                    <td className="border border-blue-600 p-2">{item.Today_Low.toFixed(2)} {item.Currency}</td>
                    <td className="border border-blue-600 p-2">{item.Current_Date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Stock Dates */}
      <h2 className="text-2xl font-bold mb-4">Stock Dates</h2>
      <div className="overflow-x-auto">
        <table className="w-full min-w-max border-collapse bg-white text-blue-800 rounded-lg shadow-md">
          <thead className="bg-blue-700 text-white">
            <tr>
              <th className="border border-blue-600 p-2">Company Name</th>
              <th className="border border-blue-600 p-2">Current Date</th>
              <th className="border border-blue-600 p-2">1 Week Ago</th>
              <th className="border border-blue-600 p-2">1 Month Ago</th>
              <th className="border border-blue-600 p-2">1 Year Ago</th>
            </tr>
          </thead>
          <tbody>
            {stockData.map((item, index) => (
              <tr key={index} className={index % 2 === 0 ? 'bg-blue-50' : 'bg-blue-100'}>
                <td className="border border-blue-600 p-2">{item.Company_Name}</td>
                <td className="border border-blue-600 p-2">{item.Current_Date}</td>
                <td className="border border-blue-600 p-2">{item["1_Week_Back_Date"]}</td>
                <td className="border border-blue-600 p-2">{item["1_Month_Back_Date"]}</td>
                <td className="border border-blue-600 p-2">{item["1_Year_Back_Date"]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
