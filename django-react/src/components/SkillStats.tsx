import { Box, Button, Flex, Heading, SimpleGrid, VStack } from "@chakra-ui/react"
import React from "react"
import axios from "axios"

export default function SkillStats() {

    const [gameSessions, setGameSessions] = React.useState([])
    const [data, setData] = React.useState<SkillData | null>(null)

    interface SkillData {
        numSessions: number,
        skillUsage: SkillUsage[],
        topSkills: SkillUsage[],
    }
    interface SkillUsage {
        skillName: string,
        skillCount: number,
        quantiles: number[],
        powerScore: number
    }

    React.useEffect(() => {
        try {
            getData()
        } catch {
            console.log("Error getting data")
        }

    }, [])

    async function getData() {
        try {
            const skillData = await axios.get<SkillData>("http://localhost:8000/api/getDoLLStats?version=1.1.4")
            setData(skillData.data)
        } catch (error) {
            console.error(error)
        }
    }

    async function getGameSessions() {
        const gameSessions = await axios.get("http://localhost:8000/api/getGameSessionData?version=1.1.4")
        setGameSessions(gameSessions.data)
    }

    console.log(data)
    console.log(gameSessions)

    return (
        <Box>
            <Button onClick={getGameSessions}>Get Game Sessions</Button>
            {data &&
                <Flex>
                    <VStack>
                        <Heading fontSize="23px">
                            Skills Ranking (95 Quartile Sorted)
                        </Heading>
                        <SimpleGrid w="700px" columns={4}>
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                Name
                            </Box>
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                Count
                            </Box>
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                95QT
                            </Box>
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                Power Score
                            </Box>
                            {
                                data.skillUsage.map((skill) => {
                                    return (
                                        <>
                                            <Box textAlign="center">
                                                {skill.skillName}
                                            </Box>
                                            <Box textAlign="center">
                                                {skill.skillCount}
                                            </Box>
                                            <Box textAlign="center">
                                                {skill.quantiles[0.95] && skill.quantiles[0.95].toFixed(2)}
                                            </Box>
                                            <Box textAlign="center">
                                                {skill.powerScore}
                                            </Box>
                                        </>
                                    )
                                })
                            }
                        </SimpleGrid>
                    </VStack>
                    <VStack>
                        <Heading fontSize="23px">
                            Top Skills (Top 20 From Leaderboard)
                        </Heading>
                        <SimpleGrid
                            w="700px"
                            columns={4}
                            ml="60px"
                        >
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                Name
                            </Box>
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                Count
                            </Box>
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                95QT
                            </Box>
                            <Box fontSize="20px" fontWeight="800" textDecoration="underline" textAlign="center">
                                Power Score
                            </Box>
                            {
                                data.topSkills.map((skill) => {
                                    return (
                                        <>
                                            <Box textAlign="center">
                                                {skill.skillName}
                                            </Box>
                                            <Box textAlign="center">
                                                {skill.skillCount}
                                            </Box>
                                            <Box textAlign="center">
                                                {skill.quantiles}
                                            </Box>
                                            <Box textAlign="center">
                                                {skill.powerScore}
                                            </Box>
                                        </>
                                    )
                                })
                            }
                        </SimpleGrid>
                    </VStack>
                </Flex>
            }
        </Box>

    )
}