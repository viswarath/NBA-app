import * as React from 'react';
import { GridColDef } from '@mui/x-data-grid';
import { DataTable } from '../DefaultTable';  

interface TradeData {
  trade_id: string;
  player1_id: string;
  new_team1_id: string;
  player2_id: string;
  new_team2_id: string;
  trade_date: string;
}

const tradeColumns: GridColDef[] = [
  { field: 'trade_id', headerName: 'Trade ID', width: 150 },
  { field: 'player1_id', headerName: 'Player 1 ID', width: 200 },
  { field: 'new_team1_id', headerName: 'New Team 1 ID', width: 150 },
  { field: 'player2_id', headerName: 'Player 2 ID', width: 200 },
  { field: 'new_team2_id', headerName: 'New Team 2 ID', width: 150 },
  { field: 'trade_date', headerName: 'Trade Date', width: 200 },
];

const fetchTrades = async () => {
  const response = await fetch('http://0.0.0.0:8000/trades');
  if (!response.ok) {
    throw new Error('Error fetching data');
  }
  return response.json();
};

interface TradeDataTableProps {
  key: number; 
}

export const TradeDataTable: React.FC<TradeDataTableProps> = ({ key }) => {
  return (
    <DataTable<TradeData>
      key={key}
      queryKey={["trades"]}
      queryFn={fetchTrades}
      columns={tradeColumns}
      label="Trade ID"
      getRowId={(row) => row.trade_id}
      disabledSearch={true}
    />
  );
};
