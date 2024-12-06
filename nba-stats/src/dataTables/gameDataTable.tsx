import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { Stack, TextField, Alert, Skeleton, Button } from '@mui/material';
import { useQuery } from '@tanstack/react-query';

interface GameData {
  home_team_id: string;
  away_team_id: string; 
  game_id: number;
  game_date: string;
  link: string;
}

interface GameStatData {
  home_team_id: string;
  away_team_id: string; 
  game_id: number;
  game_date: string;
  link: string;
  games_stat: number;
}