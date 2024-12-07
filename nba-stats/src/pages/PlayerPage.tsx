
import { Stack } from '@mui/material';
import React from 'react'
import {PlayerDataTable} from '../tables/player_tables/PlayerTable';
import { SpecializedPlayerTable } from '../tables/player_tables/SpecializedPlayerTable';

export const PlayerPage : React.FC = () => {
    return(
        <Stack spacing={3}>
            <PlayerDataTable/>
            <SpecializedPlayerTable/>
        </Stack>
    );
}