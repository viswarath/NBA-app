import * as React from 'react';
import { GridColDef } from '@mui/x-data-grid';
import { Button, Stack } from '@mui/material';
import { DataTable } from '../DefaultTable';

interface GameData {
  home_team_id: string;
  away_team_id: string; 
  game_id: number;
  game_date: string;
  link: string;
}

const normalColumns: GridColDef[] = [
  { field: 'game_id', headerName: 'Game ID', width: 150 },
  { field: 'home_team_id', headerName: 'Home Team ID', width: 150 },
  { field: 'away_team_id', headerName: 'Away Team ID', width: 150 },
  { field: 'game_date', headerName: 'Game Date', width: 180 },
  { field: 'link', headerName: 'Link', width: 500 },
];

const advancedColumns: GridColDef[] = [
  { field: 'game_id', headerName: 'Game ID', width: 120 },
  { field: 'home_team_id', headerName: 'Home Team ID', width: 120 },
  { field: 'away_team_id', headerName: 'Away Team ID', width: 120 },
  { field: 'game_date', headerName: 'Game Date', width: 140 },
  { field: 'link', headerName: 'Link', width: 300 },
  { field: 'home_team_pythagorean_wins', headerName: 'Home Team Pythagorean Wins', width: 160 },
  { field: 'home_team_schedule_strength', headerName: 'Home Team Schedule Strength', width: 180 },
  { field: 'home_team_ORTG', headerName: 'Home Team ORTG', width: 120 },
  { field: 'away_team_pythagorean_wins', headerName: 'Away Team Pythagorean Wins', width: 160 },
  { field: 'away_team_schedule_strength', headerName: 'Away Team Schedule Strength', width: 180 },
  { field: 'away_team_ORTG', headerName: 'Away Team ORTG', width: 120 },
  { field: 'arena_name', headerName: 'Arena Name', width: 160 },
  { field: 'arena_attendance', headerName: 'Arena Attendance', width: 140 },
];



const fetchGameData = async (team_id: string, isAdvanced: boolean) => {
  const endpoint = isAdvanced
    ? `http://0.0.0.0:8000/advancedGameStat`
    : `http://0.0.0.0:8000/games`;
  
  const response = await fetch(endpoint);
  if (!response.ok) {
    throw new Error('Error fetching data');
  }
  return response.json();
};

export const GameDataTable: React.FC = () => {
  const [isAdvanced, setIsAdvanced] = React.useState(false);
  const [teamId,] = React.useState<string>('');

  const handleToggle = () => {
    setIsAdvanced((prev) => !prev);
  };

  return (
    <Stack>
      <DataTable<GameData>
        queryKey={['games', isAdvanced ? "advanced" : "normal", teamId]}
        queryFn={() => fetchGameData(teamId, isAdvanced)}
        columns={isAdvanced ? advancedColumns : normalColumns}
        label="Team ID"
        getRowId={(row) => row.game_id}
        disabledSearch={true}
      />
      <Button variant="contained" onClick={handleToggle}>
        {isAdvanced ? 'Switch to Games' : 'Switch to Advanced Stats'}
      </Button>
    </Stack>
  );
};
