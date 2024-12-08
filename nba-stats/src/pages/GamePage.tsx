
import { Stack } from '@mui/material';
import React from 'react'
import { GameDataTable } from '../tables/game_tables/GameTable';

const GamePage : React.FC = () => {
    return(
        <Stack spacing={3}>
            <GameDataTable/>
        </Stack>
    );
}



export default GamePage;