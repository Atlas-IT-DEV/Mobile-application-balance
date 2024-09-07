import { useState } from "react";
import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

const FilterButton = () => {
  const [selected, setSelected] = useState([1, 0, 0]);
  return (
    <ScrollView horizontal={true} showsHorizontalScrollIndicator={false}>
      <View style={styles.container}>
        <TouchableOpacity
          style={[
            styles.button,
            selected[0] == 1 ? styles.activeButton : styles.unActiveButton,
          ]}
          onPress={() => setSelected([1, 0, 0])}
        >
          <Text
            style={[
              styles.buttonText,
              selected[0] == 1
                ? styles.activeButtonText
                : styles.unActiveButtonText,
            ]}
          >
            Новое жилье
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.button,
            selected[1] == 1 ? styles.activeButton : styles.unActiveButton,
          ]}
          onPress={() => setSelected([0, 1, 0])}
        >
          <Text
            style={[
              styles.buttonText,
              selected[1] == 1
                ? styles.activeButtonText
                : styles.unActiveButtonText,
            ]}
          >
            Расширение жилья
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.button,
            selected[2] == 1 ? styles.activeButton : styles.unActiveButton,
          ]}
          onPress={() => setSelected([0, 0, 1])}
        >
          <Text
            style={[
              styles.buttonText,
              selected[2] == 1
                ? styles.activeButtonText
                : styles.unActiveButtonText,
            ]}
          >
            Первоначальный взнос
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flexDirection: "row", gap: 20, paddingBottom: 10 },
  button: {
    height: 35,
    justifyContent: "center",
    paddingHorizontal: 15,

    borderRadius: 100,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 8,
  },
  activeButton: {
    backgroundColor: "rgba(48, 31, 129, 1)",
  },
  unActiveButton: {
    backgroundColor: "white",
  },

  buttonText: {
    fontFamily: "IBMMedium",
  },
  activeButtonText: {
    color: "rgba(255, 255, 255, 1)",
  },
  unActiveButtonText: {
    color: "rgba(22, 3, 111, 1)",
  },
});

export default FilterButton;
