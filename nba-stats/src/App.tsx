import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import {MainPage} from './mainPage'

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
        <MainPage />
    </QueryClientProvider>
  );
}

