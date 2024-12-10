import { useEffect, useState } from "react";

import Grid from "@mui/material/Grid2";


import ItemList from "./components/list";
import ActionSelect from "./components/select";
import { Item } from "./datatypes";
import axios from "axios";
import { Box } from "@mui/material";
import SearchBar from "./components/search";
import ItemCard from "./components/card";
import { DataContext, ItemContext, ItemsContext, ResultContext, ActionContext } from "./context";

const height: string = "86vh"
const leftCol: number = 3.5;

export const border: string = 'solid #D3D3D3 1px';

export default function Mobile() {
        const [searchHeight, setSearchHeight] = useState<string>("73px");

        const [action, setAction] = useState<string>('');
        const [data, setData] = useState<Array<Item>>([]);
        const [items, setItems] = useState<Array<Item>>([]);
        const [results, setResults] = useState<Array<Item>>([]);
        const [item, setItem] = useState<Item | null>(null);


        // динамичное изменение размера
        const handleResize = () => {
                const h = document.querySelector("#searchRow");
                const sh = h ? getComputedStyle(h).getPropertyValue("height") : searchHeight;
                setSearchHeight(sh);
        };
        window.addEventListener("resize", handleResize)


        useEffect(() => {
                axios.post("http://127.0.0.1:8800/mobile/example/",
                        { scheme: 10, iql: "Name LIKE !test" })
                        .then((response) => {
                                setData(response.data);
                                setItems(response.data);
                                setResults(response.data);
                        });

        }, [])

        return (
                <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%", padding: 0, margin: 0 }} >
                        <Box textAlign={"left"} sx={{ boxShadow: 8, height: height, width: "84vw" }}>
                                <DataContext.Provider value={data}>
                                        <ResultContext.Provider value={[results, setResults]} >
                                                <ItemContext.Provider value={[item, setItem]}>
                                                        <ItemsContext.Provider value={[items, setItems]}>
                                                                <ActionContext.Provider value={[action, setAction]}>
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
                                                                                        {item ? <ItemCard /> : ''}
                                                                                </Grid>

                                                                        </Grid>
                                                                </ActionContext.Provider>
                                                        </ItemsContext.Provider>
                                                </ItemContext.Provider>
                                        </ResultContext.Provider>
                                </DataContext.Provider>
                        </Box >
                </ Box>)
}
