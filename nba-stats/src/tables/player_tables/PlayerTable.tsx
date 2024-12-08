import * as React from 'react';
import { GridColDef } from '@mui/x-data-grid';
import { DataTable } from '../DefaultTable';  // Import the abstracted DataTable component

interface PlayerData {
  player_id: number;
  team_id: string;
  name: string;
  age: number;
  position: string;
  games_started: number;
}

const playerColumns: GridColDef[] = [
  { field: 'player_id', headerName: 'Player ID', width: 150 },
  { field: 'name', headerName: 'Name', width: 200 },
  { field: 'team_id', headerName: 'Team', width: 150 },
  { field: 'position', headerName: 'Position', width: 150 },
  { field: 'age', headerName: 'Age', width: 100 },
  { field: 'games_started', headerName: 'Games Started', width: 180 },
];

const fetchPlayers = async (name: string) => {
  const response = await fetch(`http://0.0.0.0:8000/players?name=${name}`);
  if (!response.ok) {
    throw new Error('Error fetching data');
  }
  return response.json();
};

export const PlayerDataTable: React.FC = () => {
  return (
    <DataTable<PlayerData>
      queryKey={['players']}
      queryFn={fetchPlayers}
      columns={playerColumns}
      label="Player Name"
      getRowId={(row) => row.player_id}  

    />
  );
};
