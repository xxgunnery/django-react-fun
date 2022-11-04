import { Box } from "@chakra-ui/react";
import axios from "axios";
import React from "react";



export default function PlayerDistribution() {

    const [data, setData] = React.useState(null)

    React.useEffect(() => {
        try {
            getData()
        } catch {
            console.log("Error getting data")
        }

    })

    async function getData() {
        const playerDistributions = await axios.get("http://localhost:8000/api/getPlayerDistributions?version=1.1.4")

        setData(playerDistributions.data)
    }

    console.log(data)
    return (
        <Box>
            Hello World
        </Box>
    )
}