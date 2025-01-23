import { useEffect, useState } from "react";
import Grid from "@mui/material/Grid2";
import CircularProgress from '@mui/material/CircularProgress';

import ItemList from "./components/list/list";
import ActionSelect from "./components/select";
import { Item } from "./datatypes";
import axios from "axios";
import { Box, IconButton } from "@mui/material";
import SearchBar from "./components/search";
import ItemCard from "./components/card";
import { DataContext, ItemContext, ItemsContext, ResultContext, ActionContext, StoresContext, LoadingContext, StoreContext, QuerryContext } from "./context";
import { Typography } from "@mui/material";

import CloseIcon from '@mui/icons-material/Close';


export const API_URL = 'http://127.0.0.1:8800/mobile';


const height: string = "86vh"
const leftCol: number = 3.5;

export const border: string = 'solid #D3D3D3 1px';

export default function Mobile() {
        const [searchHeight, setSearchHeight] = useState<string>("73px");

        const [loading, setLoading] = useState<boolean>(true);

        const [action, setAction] = useState<string>('');
        const [querry, setQuerry] = useState<string>('');
        const [data, setData] = useState<Array<Item>>([]);
        const [items, setItems] = useState<Array<Item>>([]);
        const [results, setResults] = useState<Array<Item>>([]);
        const [item, setItem] = useState<Item | null>(null);
        const [stores, setStores] = useState<Array<Item>>([]);
        const [store, setStore] = useState<string | null>(null);


        // динамичное изменение размера
        const handleResize = () => {
                const h = document.querySelector("#searchRow");
                const sh = h ? getComputedStyle(h).getPropertyValue("height") : searchHeight;
                setSearchHeight(sh);
        };
        window.addEventListener("resize", handleResize)

        useEffect(() => {
                axios.post(`${API_URL}/stores/`)
                        .then(response => {
                                setStores(response.data);
                        })
                        .finally(() => { setLoading(false); })
        }, [])

        return (
                <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%", padding: 0, margin: 0 }} >
                        <Box textAlign={"left"} sx={{ boxShadow: 8, height: height, width: "84vw" }}>
                                <DataContext.Provider value={[data, setData]}>
                                        <StoresContext.Provider value={[stores, setStores]}>
                                                <ResultContext.Provider value={[results, setResults]} >
                                                        <ItemContext.Provider value={[item, setItem]}>
                                                                <ItemsContext.Provider value={[items, setItems]}>
                                                                        <StoreContext.Provider value={[store, setStore]}>
                                                                                <ActionContext.Provider value={[action, setAction]}>
                                                                                        <QuerryContext.Provider value={[querry, setQuerry]}>
                                                                                                <LoadingContext.Provider value={[loading, setLoading]}>

                                                                                                        <Grid container id="searchRow" sx={{ borderBottom: border }} size={12}>
                                                                                                                <Grid size={leftCol} p={1}
                                                                                                                        sx={{ borderRight: border }} >
                                                                                                                        <ActionSelect />
                                                                                                                </Grid>
                                                                                                                <Grid size={12 - leftCol} p={1}>
                                                                                                                        <SearchBar />
                                                                                                                </Grid>
                                                                                                        </Grid>
                                                                                                        <Grid container size={12}>
                                                                                                                <Grid size={leftCol}
                                                                                                                        sx={{
                                                                                                                                height: `calc(${height} - ${searchHeight})`,
                                                                                                                                borderRight: border,
                                                                                                                                overflowY: "auto",
                                                                                                                                scrollbarWidth: "none"
                                                                                                                        }}>
                                                                                                                        <ItemList /></Grid>
                                                                                                                <Grid size={12 - leftCol}>
                                                                                                                        <>
                                                                                                                                <Typography textAlign={"center"}
                                                                                                                                        variant='subtitle2'
                                                                                                                                        sx={{ position: "sticky", top: 0, borderBottom: border, backgroundColor: "white" }}>
                                                                                                                                        Карточка устройства
                                                                                                                                        <IconButton
                                                                                                                                                onClick={() => { setItem(null) }}
                                                                                                                                                size={"small"}
                                                                                                                                                disabled={item === null}
                                                                                                                                                sx={{ padding: 0, position: "absolute", right: 0 }}
                                                                                                                                        >
                                                                                                                                                <CloseIcon
                                                                                                                                                        color={item !== null ? "error" : 'disabled'} />
                                                                                                                                        </IconButton>
                                                                                                                                </Typography>

                                                                                                                        </>
                                                                                                                        {item ? <ItemCard /> : ''}
                                                                                                                </Grid>

                                                                                                        </Grid>
                                                                                                </LoadingContext.Provider>
                                                                                        </QuerryContext.Provider>
                                                                                </ActionContext.Provider>
                                                                        </StoreContext.Provider>
                                                                </ItemsContext.Provider>
                                                        </ItemContext.Provider>
                                                </ResultContext.Provider>
                                        </StoresContext.Provider>
                                </DataContext.Provider>
                        </Box >
                        {loading && <CircularProgress size={'16vh'} sx={{ position: 'absolute', top: '42bv', left: "-5vh", marginLeft: "50%" }} />}
                </ Box >)
}
